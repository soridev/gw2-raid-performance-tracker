import os
import psycopg2
import datetime
import dateutil.parser
import json
import hashlib
import requests

from psycopg2.extras import execute_values

from config_helper import ConfigHelper
from application_logging import init_logger

logger = init_logger()


class ArcDataTransformator:
    def __init__(self) -> None:
        self.conf = ConfigHelper()
        self.db_connection = psycopg2.connect(
            host=self.conf.get_config_item("postgres-db", "server"),
            port=self.conf.get_config_item("postgres-db", "port"),
            database=self.conf.get_config_item("postgres-db", "database_name"),
            user=self.conf.get_config_item("postgres-db", "user"),
            password=self.conf.get_config_item("postgres-db", "password"),
        )

        self.db_connection.autocommit = True
        self.known_input_files = self.get_known_files()
        self.arc_raid_folders = []
        self.dr_user_token = self.conf.get_config_item("elite-insights", "dr_user_token")
        self.upload_logs = self.conf.get_boolean_item("elite-insights", "upload_logs")

        # fetch already registered inputfiles

    def get_known_files(self):
        known_input_files = []

        cursor = self.db_connection.cursor()
        cursor.execute(
            "select input_file from ark_core.raid_kill_times rkt group by input_file"
        )

        for line in cursor.fetchall():
            known_input_files.append(line[0])

        self.db_connection.commit()

        return known_input_files

    def get_arc_folder_names(self):
        folders = []
        cursor = self.db_connection.cursor()

        sql = "select ark_folder_name from ark_core.raid_encounters"
        cursor.execute(sql)

        for line in cursor.fetchall():
            folders.append(line[0])

        return folders

    def register_arclog_into_db(
        self, evtc_path: str, path_to_json_file: str, upload: bool = False
    ):
        evtc_name = os.path.basename(evtc_path)

        if not os.path.isfile(path_to_json_file):
            raise Exception("Given .json file does not exist.")

        if evtc_name in self.known_input_files:
            logger.info(
                f"The given input file ({path_to_json_file}) is already registered into the database"
            )

            return None

        log_data = None

        # open json-file and get data
        with open(path_to_json_file, "r", encoding="utf-8") as jsonfile:
            try:
                log_data = json.load(jsonfile)
            except Exception as err:
                logger.info(f"error while loading json from jsonfile: {str(err)}")

        # basic data from log
        file_source = evtc_name
        boss_name = log_data["fightName"]
        start_time = dateutil.parser.parse(log_data["timeStart"])
        end_time = dateutil.parser.parse(log_data["timeEnd"])
        qualifying_date = start_time.date()
        duration = datetime.datetime.strptime(
            log_data["duration"], "%Mm %Ss %fms"
        )  # e.g. 05m 50s 137ms
        duration_seconds = datetime.timedelta(
            hours=duration.hour,
            minutes=duration.minute,
            seconds=duration.second,
            microseconds=duration.microsecond,
        ).total_seconds()
        success = log_data["success"]
        is_cm = log_data["isCM"]

        # create identifier for log
        identifying_string = f"{str(boss_name)}{str(start_time)}"
        log_id = hashlib.sha1(bytes(identifying_string, encoding="utf-8")).hexdigest()

        # insert into datbase
        cursor = self.db_connection.cursor()
        self.db_connection.autocommit = False

        try:
            # basic log info
            insert_stmt = """
                INSERT INTO ark_core.raid_kill_times(
                    log_id, encounter_name, qualifying_date, start_time, end_time, kill_duration_seconds, success, cm, input_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            input_params = (
                log_id,
                boss_name,
                qualifying_date,
                start_time,
                end_time,
                duration_seconds,
                success,
                is_cm,
                file_source,
            )

            cursor.execute(insert_stmt, input_params)

            # safe player infos
            self.register_player_info(
                log_id, kill_duration=duration_seconds, json_data=log_data
            )

            # safe mechanic infos
            self.register_mechanics_info(log_id, json_data=log_data)

            self.known_input_files.append(evtc_name)
            self.db_connection.commit()

            logger.info("Registered log into the database.")

            if self.upload_logs:
                try:
                    self.upload_log(evtc_path, log_id=log_id)
                except Exception as uperr:
                    logger.error(f"Unable to upload log to dps.report: {str(uperr)}")

            # cleanup file after usage.
            logger.info(f"removing .json file: {str(path_to_json_file)}")
            os.remove(path_to_json_file)

            return log_id

        except Exception as err:
            self.db_connection.rollback()

            raise err

    def register_player_info(self, log_id, kill_duration, json_data):
        # player and class info
        log_data = json_data
        cursor = self.db_connection.cursor()
        players = log_data["players"]

        insert_stmt = """
            INSERT INTO ark_core.player_info
                (log_id, account_name, character_name, profession, target_dps, total_cc, downstates, died)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for p in players:
            paccount = p["account"]
            pname = p["name"]
            pprofession = p["profession"]
            # dps targets contains all targets => index 0 is always the boss, next we get list of phases => index 0 is total (all phases)
            target_dps = p["dpsTargets"][0][0]["dps"]
            total_cc = p["dpsTargets"][0][0]["breakbarDamage"]
            downstates = 0
            died = False

            # check mechanics
            for item in log_data["mechanics"]:
                if item["name"] == "Downed":
                    for entry in item["mechanicsData"]:
                        if entry["actor"] == pname:
                            downstates += 1

                # check if player died
                if item["name"] == "Dead":
                    for entry in item["mechanicsData"]:
                        if entry["actor"] == pname:
                            if entry["time"] <= kill_duration * 1000:
                                died = True

            params = (
                log_id,
                paccount,
                pname,
                pprofession,
                target_dps,
                total_cc,
                downstates,
                died,
            )

            cursor.execute(insert_stmt, params)

    def register_mechanics_info(self, log_id, json_data):
        cursor = self.db_connection.cursor()
        log_data = json_data

        # get all infos about mechanics from the log
        ignore_list = ["Dead", "Downed", "Res", "Got up"]
        mech_list = []
        encounter_name = log_data["fightName"]

        for item in log_data["mechanics"]:
            if item["name"] in ignore_list:
                pass
            else:
                current_mech_name = item["name"]
                current_mech_description = item["description"]

                for item_detail in item["mechanicsData"]:
                    time_info = int(item_detail["time"])
                    affected_actor = item_detail["actor"]

                    new_entry = (
                        log_id,
                        encounter_name,
                        current_mech_name,
                        current_mech_description,
                        time_info,
                        affected_actor,
                    )

                    if new_entry not in mech_list:
                        mech_list.append(new_entry)

        # insert the data into the db
        insert_sql = """
                        INSERT INTO ARK_CORE.MECHANIC_INFO (
                            LOG_ID,
                            ENCOUNTER_NAME,
                            MECHANIC_NAME,
                            MECHANIC_DESCRIPTION,
                            TIME_INFO,
                            ACTOR)
                        VALUES %s
        """

        execute_values(cursor, insert_sql, mech_list)

    def upload_log(self, log_path: str, log_id: str):
        """Uploads an arcdps log do dps.report and adds the link in the database to the registered log"""

        try:

            base_url = f"""https://dps.report/uploadContent?json=1&generator=ei&userToken={self.dr_user_token}"""
            form_data = {
                'file': (os.path.basename(log_path), open(log_path, 'rb')),
                'action': (None, 'store'),
                'path': (None, '/path1')
            }

            r = requests.post(base_url, files=form_data).json()
            permalink = r["permalink"]

            update_sql = """
                            UPDATE ARK_CORE.RAID_KILL_TIMES SET LINK_TO_UPLOAD = %s
                            WHERE LOG_ID = %s
            """

            cursor = self.db_connection.cursor()
            cursor.execute(query=update_sql, vars=(permalink, log_id))
            self.db_connection.commit()

            logger.info("Successfuly uploaded log to dps.report.")

        except Exception as err:
            logger.error("An error occured when uploading a log to dps.report:")
            logger.error(f"{str(err)}")
            raise Exception("Upload failed. Check log for details.")


def main():
    print("This should be used as a library.")


if __name__ == "__main__":
    main()
