import sys
import os
import subprocess
import shlex
import configparser
from application_logging import init_logger

logger = init_logger()


def generate_raw_data(file_path: str, settings_file: str, base_path: str):

    if not os.path.exists(file_path):
        raise Exception("the log-file you are trying to parse does not exist.")

    if not os.path.exists(settings_file):
        logger.info(settings_file)
        raise Exception(
            "the ELITE INSIGHTS settings-file you are trying to load does not exist."
        )

    ie_binary = os.path.join(base_path, r"GW2EI\GuildWars2EliteInsights.exe")

    if not os.path.exists(ie_binary):
        raise Exception(
            "Could not find the Elite Insights binary at the specified path."
        )

    logger.info(f"Parsing .json from input file: {str(file_path)}")

    cmd = f'{ie_binary} -c "{settings_file}" "{file_path}"'
    cmd = cmd.replace("\\", "/")

    proc = subprocess.Popen(
        shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (stderr, stdout) = proc.communicate()

    if proc.returncode != 0:
        logger.info(stderr)
        logger.info(stdout)
