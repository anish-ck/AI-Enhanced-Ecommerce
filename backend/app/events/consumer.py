import json
import logging

from kafka import KafkaConsumer

from app.core import config

logger = logging.getLogger("app.events")


def get_consumer() -> KafkaConsumer:
    if not (
        config.EVENT_HUB_BOOTSTRAP_SERVER
        and config.EVENT_HUB_CONNECTION_STRING
        and config.EVENT_HUB_TOPIC
    ):
        raise RuntimeError("Event hub config missing")

    return KafkaConsumer(
        config.EVENT_HUB_TOPIC,
        bootstrap_servers=config.EVENT_HUB_BOOTSTRAP_SERVER,
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username="$ConnectionString",
        sasl_plain_password=config.EVENT_HUB_CONNECTION_STRING,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="ecommerce-local-consumer",
        enable_auto_commit=True,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    consumer = get_consumer()
    logger.info("Consumer started")

    for message in consumer:
        print("Received event:", message.value)


if __name__ == "__main__":
    main()
