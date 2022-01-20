import json
import sys
import configparser
import os
import time

import kafka

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps

from arc_log_generator import generate_raw_data


class ArcWatchDog:
    def __init__(self, logpath:str) -> None:
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
        except:
            self.observer.stop()
            print("stopped watching.")

        self.observer.join()

class Handler(FileSystemEventHandler):
    
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Found newly created file:  % s." % event.src_path)

            # generate json file with elite insights parser
            generate_raw_data(event.src_path, ei_settings_file, base_path)
            input_file_name = str.split(os.path.basename(event.src_path), ".")[0]

            json_result = find_file_by_name(input_file_name, os.path.join(base_path, "resources"))
            json_result_file = None

            if len(json_result) == 1:
                json_result_file = json_result[0]
            else:
                raise Exception("Seems like we have duplicate .json files in the /resources folder.")
            
            # push info into kafka stream
            kafka_message = {'input-file': event.src_path, 'ei-json-file': json_result_file}
            produce_message(kafka_bootstrap_servers, arc_topic, kafka_message)

            print("successfuly pushed message into kafka stream.")
        
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            pass


def produce_message(bootstrap_servers, topic_name, message):
    k_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    k_producer.send(topic_name, value=message)


def find_file_by_name(name, path):
    result = []    
    for root, dirs, files in os.walk(path):        
        for item in files:
            if name in item:
                result.append(os.path.join(root, item))

    return result


def main():
    global base_path
    base_path = os.path.dirname(__file__)    

    config = configparser.ConfigParser()
    config.read(os.path.join(base_path, 'config.ini'))            
    
    # load kafka config from file
    global ei_settings_file
    global arc_base_dir
    global kafka_bootstrap_servers
    global arc_topic
    
    kafka_bootstrap_servers = loads(config['kafka']['BootstrapServers'])    
    arc_topic = config.get("kafka", "ArcTopic")
    ei_settings_file = os.path.join(base_path, config.get("elite-insights", "ei_config_file"))
    arc_base_dir = config.get("elite-insights", "logfolder")


    # start filesystem watcher
    wd = ArcWatchDog(arc_base_dir)
    wd.run()

if __name__ == "__main__":
    main()