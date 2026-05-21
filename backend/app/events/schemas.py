from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_event_metadata() -> dict:
    """Return standard event metadata for observability and lineage."""
    return {
        "event_id": str(uuid4()),
        "event_version": "v1",
        "event_source": "fastapi-backend",
        "timestamp": utc_now_iso(),
    }


class BaseEvent(BaseModel):
    event_type: str
    # Event IDs allow traceability across services and retries.
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    # Versioning protects downstream consumers when schemas evolve.
    event_version: str = "v1"
    # Source tagging preserves lineage for lakehouse ingestion.
    event_source: str = "fastapi-backend"
    timestamp: str = Field(default_factory=utc_now_iso)


class ProductViewEvent(BaseEvent):
    event_type: str = "product_view"
    user_id: int
    product_id: int


class AddToCartEvent(BaseEvent):
    event_type: str = "add_to_cart"
    user_id: int
    product_id: int
    quantity: int


class CheckoutCompletedEvent(BaseEvent):
    event_type: str = "checkout_completed"
    user_id: int
    order_id: int
    total_amount: float
