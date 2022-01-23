import sys
import os
import time
import threading

import kafka

from arc_kafka_consumer import run_consumer
from arc_kafka_producer import run_producer


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


def main():
    tm = ThreadManger()
    tm.run_application()


if __name__ == "__main__":
    main()
