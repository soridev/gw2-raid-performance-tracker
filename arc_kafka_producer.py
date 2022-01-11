import json
import sys
import configparser
import os
from kafka import KafkaConsumer, KafkaProducer
import json
from json import loads, dumps

def produce_message(bootstrap_servers, topic_name):
    k_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    k_producer.send(topic_name, value={'1': 'test'})


def main():
    base_path = os.path.dirname(__file__)    

    config = configparser.ConfigParser()
    config.read(os.path.join(base_path, 'config.ini'))            
    
    # load kafka config from file
    kafka_bootstrap_servers = loads(config['kafka']['BootstrapServers'])    
    arc_topic = config.get("kafka", "ArcTopic")
    
    produce_message(kafka_bootstrap_servers, arc_topic)

if __name__ == "__main__":
    main()