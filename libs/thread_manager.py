import subprocess
import shlex
import os
import threading

from celery import chain
from config_helper import ConfigHelper
from application_logging import init_logger

from arc_data_producer import run_producer
from arc_data_transformator import ArcDataTransformator
from tasks import generate_evtc_raw_data, json_to_rdbms

logger = init_logger()


class ThreadManger:
    def __init__(
        self,
        upload_logs: bool = False,
        full_log_load: bool = False,
    ) -> None:

        self.upload_logs = upload_logs
        self.full_log_load = full_log_load

        if self.upload_logs:
            ConfigHelper().set_config_item("elite-insights", "upload_logs", "yes")
        else:
            ConfigHelper().set_config_item("elite-insights", "upload_logs", "no")

    def run_application(self):
        """Starts up the configured background tasks in seperate threads and processes."""

        if self.full_log_load:
            self.load_all_logs()
            return

        # start actions from here and do extra actiopns if specified
        arc_producer_thread = threading.Thread(target=run_producer, name="arc_json_producer")

        # start arc filewatcher
        arc_producer_thread.start()

        # subprocess.Popen(shlex.split(f"""python3 "{script_location}" --guild "{self.guild}" --fc-dates "{fc_dates}" """),shell=False)

    def load_all_logs(self):
        arc_base_dir = ConfigHelper().get_config_item("elite-insights", "logfolder")
        ei_settings_file = ConfigHelper().get_config_item("elite-insights", "ei_config_file")

        adt = ArcDataTransformator()
        unknown_files = []

        for root, directories, files in os.walk(arc_base_dir):
            for file in files:
                if file.endswith(".zevtc") and file not in adt.known_input_files:
                    unknown_files.append(os.path.join(root, file))

        logger.info(f"Found {len(unknown_files)} not registered arcdps logfiles.")

        # we execute in chunks of 10 so celery does not do weird shit.
        task_pool = []
        counter = 0

        for file in unknown_files:
            logger.info(f"Pushing file {str(file)} into queue.")
            counter += 1

            task_pool.append(
                chain(
                    generate_evtc_raw_data.s(
                        input_file_name=str.split(os.path.basename(file), ".")[0],
                        file_path=file,
                        settings_file=ei_settings_file,
                    ),
                    json_to_rdbms.s(),
                ).apply_async()
            )

            # after all workers are doing work wait for result batch. Then reset counter.
            if counter >= 12:
                for rtask in task_pool:
                    rtask.get()

                counter = 0

        logger.info("Finished scanning the log-directory.")


def sync_arc_folder():

    # find wincbtlogs/ -name \*.zevtc | rsync -av --files-from - --no-relative . uncategorized/

    return


def main():
    tm = ThreadManger(upload_logs=True, full_log_load=False)

    tm.run_application()
    # tm.load_all_logs()


if __name__ == "__main__":
    main()
