import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer
from json import dumps
from arc_log_generator import generate_raw_data
from config_helper import ConfigHelper
from application_logging import init_logger

logger = init_logger()


class ArcWatchDog:
    def __init__(self, logpath: str) -> None:
        self.observer = Observer()
        self.logpath = logpath

        if not os.path.isdir(logpath):
            raise Exception("Given log directory does not exist.")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.logpath, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except Exception as err:
            self.observer.stop()
            logger.info("stopped watching.\n" + str(err))

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        if event.event_type == "created" or event.event_type == "moved":

            full_path = None

            if event.event_type == "created":
                fname, fext = os.path.splitext(event.src_path)
                if fext != ".zevtc":
                    return
                else:
                    full_path = event.src_path

            elif event.event_type == "moved":
                fname, fext = os.path.splitext(event.dest_path)
                if fext != ".zevtc":
                    return
                else:
                    full_path = event.dest_path

            # Event is created, you can process it now
            logger.info("Found newly created file:  % s." % full_path)

            # generate json file with elite insights parser
            ei_settings_file = os.path.join(
                base_path,
                ConfigHelper().get_config_item(
                    "elite-insights",
                    "ei_config_file",
                ),
            )
            generate_raw_data(full_path, ei_settings_file, base_path)
            input_file_name = str.split(os.path.basename(full_path), ".")[0]

            json_result = find_file_by_name(input_file_name, os.path.join(base_path, "resources"))
            json_result_file = None

            if len(json_result) == 1:
                json_result_file = json_result[0]
            else:
                raise Exception("Seems like we have duplicate .json files in the /resources folder.")

            # push info into kafka stream
            kafka_bootstrap_servers = ConfigHelper().get_kafka_bootstrap_servers()
            arc_topic = ConfigHelper().get_config_item(
                "kafka",
                "ArcTopic",
            )

            # crate a message for the kafka stream
            kafka_message = {
                "id": time.time(),
                "input-file": full_path,
                "ei-json-file": json_result_file,
            }

            produce_message(kafka_bootstrap_servers, arc_topic, kafka_message)


def produce_message(bootstrap_servers, topic_name, message):
    k_producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )
    k_producer.send(topic_name, value=message)

    logger.info(f"successfuly pushed message into kafka [topic => {str(topic_name)}].")


def find_file_by_name(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        for item in files:
            if name in item:
                result.append(os.path.join(root, item))

    return result


def run_producer():
    global base_path
    base_path = os.path.dirname(__file__)

    arc_base_dir = ConfigHelper().get_config_item(
        "elite-insights",
        "logfolder",
    )

    # start filesystem watcher
    logger.info("Starting filesystem monitoring for kafka producer.")
    wd = ArcWatchDog(arc_base_dir)
    wd.run()


def main():
    # start the producer
    run_producer()


if __name__ == "__main__":
    main()
