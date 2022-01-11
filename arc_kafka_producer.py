import json
import sys
import configparser
import os
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps

from arc_log_generator import generate_raw_data

def produce_message(bootstrap_servers, topic_name):
    k_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    k_producer.send(topic_name, value={'logname': 'path-to-json-file'})

def test_logfile(ei_settings_file, base_path):

    logfile = r'C:\Users\Daniel\Documents\Guild Wars 2\addons\arcdps\arcdps.cbtlogs\Arkk\20211113-210342.zevtc'
    generate_raw_data(logfile, ei_settings_file, base_path)


def main():
    base_path = os.path.dirname(__file__)    

    config = configparser.ConfigParser()
    config.read(os.path.join(base_path, 'config.ini'))            
    
    # load kafka config from file
    kafka_bootstrap_servers = loads(config['kafka']['BootstrapServers'])    
    arc_topic = config.get("kafka", "ArcTopic")
    ei_settings_file = os.path.join(base_path, config.get("elite-insights", "ei_config_file"))
    
    print(ei_settings_file)

    test_logfile(ei_settings_file, base_path)

    # produce_message(kafka_bootstrap_servers, arc_topic)

if __name__ == "__main__":
    main()