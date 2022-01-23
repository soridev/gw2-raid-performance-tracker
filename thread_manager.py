import sys
import os
import time
import threading

import kafka

from config_helper import ConfigHelper

from arc_kafka_consumer import run_consumer
from arc_kafka_producer import run_producer

from arc_log_generator import generate_raw_data
from arc_data_transformator import ArcDataTransformator


class ThreadManger:
    def __init__(
        self,
        with_discord: bool = False,
        upload_logs: bool = False,
        full_log_load: bool = False,
    ) -> None:

        self.with_discord = with_discord
        self.upload_logs = upload_logs
        self.full_log_load = full_log_load

    def run_application(self):

        if self.full_log_load:
            self.full_log_load()

        # start actions from here and do extra actiopns if specified
        kafka_arc_consumer_thread = threading.Thread(
            target=run_consumer, name="kafka_arc_json_consumer"
        )

        kafka_arc_producer_thread = threading.Thread(
            target=run_producer, name="kafka_arc_json_producer"
        )

        # start arc_log kafka application
        kafka_arc_consumer_thread.start()
        kafka_arc_producer_thread.start()

        if self.with_discord:
            pass

    def load_all_logs(self):
        base_path = os.path.dirname(__file__)
        arc_base_dir = ConfigHelper().get_config_item(
            "elite-insights",
            "logfolder",
        )

        adt = ArcDataTransformator()
        unknown_files = []

        for root, directories, files in os.walk(arc_base_dir):
            for file in files:
                if file.endswith(".zevtc") and file not in adt.known_input_files:
                    unknown_files.append(os.path.join(root, file))

        print(len(unknown_files))


def main():
    tm = ThreadManger()
    # tm.run_application()
    tm.load_all_logs()


if __name__ == "__main__":
    main()
