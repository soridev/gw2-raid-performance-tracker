from os import path
from kafka import KafkaConsumer
from json import loads

from config_helper import ConfigHelper
from arc_data_transformator import ArcDataTransformator
from application_logging import init_logger

logger = init_logger()


def consume_messages(bt_servers, kafka_topic):
    k_consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=bt_servers,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        # consumer_timeout_ms=1000,
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )

    logger.info("Starting kafka consumer - waiting for new messages.")

    new_log_ids = []
    ark_transformator = ArcDataTransformator()

    for message in k_consumer:
        message_content = message.value
        logger.info(message_content["id"])

        log_id = ark_transformator.register_arclog_into_db(
            evtc_name=message_content["input-file"],
            path_to_json_file=message_content["ei-json-file"],
        )

        new_log_ids.append(log_id)

    logger.info(f"{len(new_log_ids)} new logs added to database.")


def run_consumer():
    kafka_bootstrap_servers = ConfigHelper().get_kafka_bootstrap_servers()
    arc_topic = ConfigHelper().get_config_item("kafka", "ArcTopic")

    consume_messages(kafka_bootstrap_servers, arc_topic)


def main():
    # start the kafka consumer.
    run_consumer()


if __name__ == "__main__":
    main()
