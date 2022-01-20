import sys
import os
import configparser
from kafka import KafkaConsumer, KafkaProducer
from json import loads

from config_helper import ConfigHelper

def consume_messages(bt_servers, kafka_topic):
    k_consumer = KafkaConsumer(kafka_topic,
                               bootstrap_servers=bt_servers,
                               auto_offset_reset='earliest',
                               enable_auto_commit=True,
                               consumer_timeout_ms=1000,
                               value_deserializer=lambda x: loads(x.decode('utf-8')))


    print("we are waiting for messages")

    for message in k_consumer:
        info = message.value
        print(str(info))

def main():
    base_path = os.path.dirname(__file__)    
    config = configparser.ConfigParser()
    config.read(os.path.join(base_path, 'config.ini'))            

    # load settings for kafka infrastructure from settings file
    kafka_bootstrap_servers = loads(config['kafka']['BootstrapServers'])    
    arc_topic = config.get("kafka", "ArcTopic")

    consume_messages(kafka_bootstrap_servers, arc_topic)

if __name__ == "__main__":
    main()