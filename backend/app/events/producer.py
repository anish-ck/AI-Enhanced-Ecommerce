import json
import logging
from typing import Any

from kafka import KafkaProducer

from app.core import config

logger = logging.getLogger("app.events")

_producer: KafkaProducer | None = None


def _config_ready() -> bool:
    return bool(
        config.EVENT_HUB_BOOTSTRAP_SERVER
        and config.EVENT_HUB_CONNECTION_STRING
        and config.EVENT_HUB_TOPIC
    )


def get_producer() -> KafkaProducer | None:
    global _producer

    if _producer is not None:
        return _producer

    if not _config_ready():
        logger.warning("Event hub config missing; producer disabled")
        return None

    _producer = KafkaProducer(
        bootstrap_servers=config.EVENT_HUB_BOOTSTRAP_SERVER,
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username="$ConnectionString",
        sasl_plain_password=config.EVENT_HUB_CONNECTION_STRING,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda value: value.encode("utf-8") if value else None,
        retries=3,
        linger_ms=5,
        acks="all",
    )
    return _producer


def publish_event(event: Any, key: str | None = None) -> None:
    try:
        producer = get_producer()
        if not producer:
            return

        payload = event.model_dump() if hasattr(event, "model_dump") else event
        event_type = payload.get("event_type", "unknown")
        future = producer.send(config.EVENT_HUB_TOPIC, value=payload, key=key)
        future.add_callback(
            lambda meta: logger.info("Published %s event to %s", event_type, meta.topic)
        )
        future.add_errback(
            lambda exc: logger.error("Failed to publish %s event: %s", event_type, exc)
        )
    except Exception:
        logger.exception("Event publish failed")
