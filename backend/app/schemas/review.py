from datetime import datetime

from pydantic import BaseModel, ConfigDict, conint


class ReviewBase(BaseModel):
    product_id: int
    rating: conint(ge=1, le=5)
    review_text: str


class ReviewCreate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
