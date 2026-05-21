from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseEvent(BaseModel):
    event_type: str
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
