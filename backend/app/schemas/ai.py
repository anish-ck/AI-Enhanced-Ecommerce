from typing import List, Optional

from pydantic import BaseModel, Field


class AIGenerateResponse(BaseModel):
    ai_title: str = Field(..., min_length=1)
    ai_description: str = Field(..., min_length=1)
    ai_category: str = Field(..., min_length=1)
    ai_tags: List[str] = Field(default_factory=list)


class AIGenerateResult(AIGenerateResponse):
    product_id: Optional[int] = None
