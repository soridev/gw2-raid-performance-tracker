import os
import psycopg2
import datetime
import dateutil.parser
import json
import hashlib

from config_helper import ConfigHelper


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
        self, evtc_name: str, path_to_json_file: str, upload: bool = False
    ):

        evtc_name = os.path.basename(evtc_name)

        if not os.path.isfile(path_to_json_file):
            raise Exception("Given .json file does not exist.")

        if evtc_name in self.known_input_files:
            print(
                f"The given input file ({path_to_json_file}) is already registered into the database"
            )

            return None

        log_data = None

        # open json-file and get data
        with open(path_to_json_file, "r", encoding="utf-8") as jsonfile:
            try:
                log_data = json.load(jsonfile)
            except Exception as err:
                print(f"error while loading json from jsonfile: {str(err)}")

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

            # player and class info
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
                                if entry["time"] <= duration_seconds * 1000:
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

            self.known_input_files.append(evtc_name)
            self.db_connection.commit()

            # cleanup file after usage.
            os.remove(path_to_json_file)

            return log_id

        except Exception as err:
            self.db_connection.rollback()

            raise err


def main():
    adt = ArcDataTransformator()
    f_id = adt.register_arclog_into_db(
        evtc_name="C:\\Users\\Daniel\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs\\Slothasor\\20211115-203047.zevtc",
        path_to_json_file="c:\\Library\\Code\\gw2-raid-performance-tracker\\resources\\20211115-203047_sloth_fail.json",
        upload=False,
    )

    print(f_id)


if __name__ == "__main__":
    main()
