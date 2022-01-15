import sys
import os
from kafka import KafkaConsumer, KafkaProducer
from json import loads


def consume_messages():
    k_consumer = KafkaConsumer('arclogs',
                               bootstrap_servers=['<string>', '<string>'],
                               auto_offset_reset='earliest',
                               enable_auto_commit=True,
                               consumer_timeout_ms=1000,
                               value_deserializer=lambda x: loads(x.decode('utf-8')))


    print("we are waiting for messages")

    for message in k_consumer:
        info = message.value
        print(str(info))

def main():
    consume_messages()

if __name__ == "__main__":
    main()