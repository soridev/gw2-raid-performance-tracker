import os
import shlex
import subprocess
import shutil

from celery import Celery
from config_helper import ConfigHelper
from application_logging import init_logger
from arc_data_transformator import ArcDataTransformator

rabbitmq_connection_string = f"""amqp://{ConfigHelper().get_config_item("rabbitmq","user")}:
{ConfigHelper().get_config_item("rabbitmq", "password")}@{ConfigHelper().get_config_item("rabbitmq", "server")}:
{ConfigHelper().get_config_item("rabbitmq", "port")}/{ConfigHelper().get_config_item("rabbitmq", "vhost")}"""

gw2_raid_performance_tracker = Celery("tasks", broker=rabbitmq_connection_string, backend="db+sqlite:///results.sqlite")


@gw2_raid_performance_tracker.task
def generate_evtc_raw_data(input_file_name: str, file_path: str, settings_file: str):
    """Generates a .json file from an .evtc log by calling the c# application GuildWars2EliteInsights.exe through mono on linux. yes i know. :-)"""

    logger = init_logger()

    def find_file_by_name(name, path):
        result = []
        for root, dirs, files in os.walk(path):
            for item in files:
                if name in item:
                    result.append(os.path.join(root, item))

        return result

    ei_binary = ConfigHelper().get_config_item("elite-insights", "binary")
    archive = ConfigHelper().get_config_item("elite-insights", "archive")
    outfolder = ConfigHelper().get_config_item("elite-insights", "outfolder")
    cmd = f"mono {ei_binary} -p -c {settings_file} {file_path}"
    basename = os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise Exception("the log-file you are trying to parse does not exist.")

    if not os.path.exists(settings_file):
        logger.info(settings_file)
        raise Exception("the ELITE INSIGHTS settings-file you are trying to load does not exist.")

    if not os.path.exists(ei_binary):
        raise Exception("Could not find the Elite Insights binary at the specified path.")

    logger.info(f"Parsing .json from input file: {str(file_path)}")

    proc = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stderr, stdout) = proc.communicate()

    if proc.returncode != 0:
        logger.info(stderr.decode())
        logger.info(stdout.decode())

    if "Parsing Failure" in stderr.decode():
        logger.info(f"Unable to parse file {file_path} - ignoring.")
        shutil.move(file_path, os.path.join(archive, basename))

        return {"input_file": None, "ei_json_file": None}

    json_result = find_file_by_name(input_file_name, outfolder)
    json_result_file = None

    if len(json_result) == 0:
        raise Exception(f".json file ({input_file_name}) not found!")
    elif len(json_result) == 1:
        json_result_file = json_result[0]
    else:
        raise Exception(f"Seems like we have duplicate .json files in the output folder ({outfolder}).")

    # move input file to archive after json is generated.
    shutil.move(file_path, os.path.join(archive, basename))

    return {"input_file": input_file_name, "ei_json_file": json_result_file}


@gw2_raid_performance_tracker.task
def json_to_rdbms(file_info):
    """Loads a json strucuture from the given location and loads it into a datamodel in a rdbms."""

    if file_info["ei_json_file"] is None:
        return None

    ark_transformator = ArcDataTransformator()

    input_filename = file_info["input_file"]
    json_file = file_info["ei_json_file"]

    log_id = ark_transformator.register_arclog_into_db(
        evtc_path=input_filename,
        path_to_json_file=json_file,
    )

    return log_id
