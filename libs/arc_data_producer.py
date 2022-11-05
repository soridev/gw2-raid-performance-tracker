import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tasks import generate_evtc_raw_data, json_to_rdbms
from application_logging import init_logger
from config_helper import ConfigHelper
from celery import chain

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
            ei_settings_file = ConfigHelper().get_config_item("elite-insights", "ei_config_file")

            input_file_name = str.split(os.path.basename(full_path), ".")[0]
            chain(
                generate_evtc_raw_data.s(
                    input_file_name=input_file_name, file_path=full_path, settings_file=ei_settings_file
                ),
                json_to_rdbms.s(),
            ).apply_async()


def run_producer():

    arc_base_dir = ConfigHelper().get_config_item("elite-insights", "logfolder")

    # start filesystem watcher
    logger.info("Starting filesystem monitoring for kafka producer.")
    wd = ArcWatchDog(arc_base_dir)
    wd.run()


def main():
    run_producer()


if __name__ == "__main__":
    main()
