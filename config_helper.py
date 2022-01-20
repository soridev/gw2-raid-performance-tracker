import os
import configparser

from json import loads

class ConfigHelper:
    def __init__(self) -> None:
        self.base_path = os.path.dirname(__file__)    
        self.config_parser = configparser.ConfigParser()
        
        # read configfile
        self.config_parser.read(os.path.join(self.base_path, 'config.ini'))            

    def get_kafka_bootstrap_servers(self):
        return loads(self.config_parser.get("kafka", "BootstrapServers"))

    def get_config_item(self, group_name:str, item_name:str):

        if group_name is None:
            return self.config_parser.get(item_name)
        else:
            return self.config_parser.get(group_name, item_name)
