import os
import configparser

from json import loads


class ConfigHelper:
    def __init__(self) -> None:
        self.base_path = os.path.dirname(__file__)
        self.config_parser = configparser.ConfigParser()
        self.config_file_path = os.path.join(self.base_path, "config.ini")

        # read configfile
        self.config_parser.read(self.config_file_path)

    def get_kafka_bootstrap_servers(self):
        return loads(self.config_parser.get("kafka", "BootstrapServers"))

    def get_config_item(self, group_name: str, item_name: str):

        if group_name is None:
            return self.config_parser.get(item_name)
        else:
            return self.config_parser.get(group_name, item_name)

    def get_boolean_item(self, group_name: str, item_name: str):
        if group_name is None:
            return self.config_parser.getboolean(item_name)
        else:
            return self.config_parser.getboolean(group_name, item_name)

    def set_config_item(self, group_name: str, item_name: str, new_value):
        self.config_parser.set(group_name, item_name, value=new_value)

        with open(self.config_file_path, "w") as configfile:
            self.config_parser.write(configfile)
