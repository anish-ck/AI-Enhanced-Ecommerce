import json
import logging
import time
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


def publish_event(event: Any, key: str | None = None, max_retries: int = 3) -> None:
    try:
        producer = get_producer()
        if not producer:
            return

        payload = event.model_dump() if hasattr(event, "model_dump") else event
        event_type = payload.get("event_type", "unknown")
        event_id = payload.get("event_id", "unknown")

        for attempt in range(1, max_retries + 1):
            try:
                future = producer.send(config.EVENT_HUB_TOPIC, value=payload, key=key)
                metadata = future.get(timeout=10)
                logger.info(
                    "event_publish_success event_id=%s event_type=%s topic=%s partition=%s offset=%s",
                    event_id,
                    event_type,
                    metadata.topic,
                    metadata.partition,
                    metadata.offset,
                )
                return
            except Exception as exc:
                logger.warning(
                    "event_publish_retry event_id=%s event_type=%s attempt=%s error=%s",
                    event_id,
                    event_type,
                    attempt,
                    exc,
                )
                time.sleep(0.2 * attempt)

        logger.error(
            "event_publish_failed event_id=%s event_type=%s retries=%s",
            event_id,
            event_type,
            max_retries,
        )
    except Exception:
        logger.exception("event_publish_exception")
