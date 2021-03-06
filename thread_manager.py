import subprocess
import shlex
import os
import threading

from config_helper import ConfigHelper
from application_logging import init_logger

from arc_kafka_consumer import run_consumer
from arc_kafka_producer import run_producer, find_file_by_name

from arc_log_generator import generate_raw_data
from arc_data_transformator import ArcDataTransformator

from discord_interactions import startup_fc_watcher

logger = init_logger()


class ThreadManger:
    def __init__(
        self,
        with_discord: bool = False,
        upload_logs: bool = False,
        fullclear_dates: str = None,
        guild: str = None,
        full_log_load: bool = False,
    ) -> None:

        self.with_discord = with_discord
        self.upload_logs = upload_logs
        self.fullclear_dates = fullclear_dates
        self.guild = guild
        self.full_log_load = full_log_load

        if self.upload_logs:
            ConfigHelper().set_config_item("elite-insights", "upload_logs", "yes")
        else:
            ConfigHelper().set_config_item("elite-insights", "upload_logs", "no")

    def run_application(self):
        """Starts up the configured background tasks in seperate threads or processes."""

        if self.full_log_load:
            self.load_all_logs()
            return

        # start actions from here and do extra actiopns if specified
        kafka_arc_consumer_thread = threading.Thread(target=run_consumer, name="kafka_arc_json_consumer")
        kafka_arc_producer_thread = threading.Thread(target=run_producer, name="kafka_arc_json_producer")

        # start arc_log kafka application
        kafka_arc_consumer_thread.start()
        kafka_arc_producer_thread.start()

        if self.with_discord and self.fullclear_dates and self.guild:
            fc_dates = ",".join(str(item) for item in self.fullclear_dates)
            script_location = os.path.join(os.path.dirname(__file__), "discord_interactions.py").replace("\\", "/")

            subprocess.Popen(
                shlex.split(f"""python "{script_location}" --guild "{self.guild}" --fc-dates "{fc_dates}" """),
                shell=False,
            )

    def load_all_logs(self):
        base_path = os.path.dirname(__file__)
        arc_base_dir = ConfigHelper().get_config_item(
            "elite-insights",
            "logfolder",
        )

        ei_settings_file = os.path.join(
            base_path,
            ConfigHelper().get_config_item(
                "elite-insights",
                "ei_config_file",
            ),
        )

        adt = ArcDataTransformator()
        arc_folder_names = adt.get_arc_folder_names()
        unknown_files = []

        for root, directories, files in os.walk(arc_base_dir):
            for file in files:
                for arc_folder in arc_folder_names:
                    if arc_folder in root:
                        if file.endswith(".zevtc") and file not in adt.known_input_files:
                            unknown_files.append(os.path.join(root, file))

        logger.info(f"Found {len(unknown_files)} not registered arcdps logfiles.")

        for file in unknown_files:
            logger.info(f"Generating json-file for logfile: {str(file)}")
            generate_raw_data(file_path=file, settings_file=ei_settings_file, base_path=base_path)

            input_file_name = str.split(os.path.basename(file), ".")[0]

            json_result = find_file_by_name(input_file_name, os.path.join(base_path, "resources"))
            json_result_file = None

            if len(json_result) == 1:
                json_result_file = json_result[0]
            else:
                raise Exception("Seems like we have duplicate .json files in the /resources folder.")

            logger.info("registering .json file into the database")
            adt.register_arclog_into_db(evtc_path=file, path_to_json_file=json_result_file, upload=False)


def main():
    tm = ThreadManger(
        with_discord=False,
        upload_logs=True,
        fullclear_dates=["2022-02-14"],
        guild="ZETA",
        full_log_load=False,
    )

    tm.run_application()
    # tm.load_all_logs()


if __name__ == "__main__":
    main()
