from fastapi import APIRouter, HTTPException
import httpx

from app.core import config
from app.schemas.analytics import AnalyticsQueryRequest, AnalyticsQueryResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/query", response_model=AnalyticsQueryResponse)
async def proxy_analytics_query(
    payload: AnalyticsQueryRequest,
) -> AnalyticsQueryResponse:
    url = f"{config.ANALYTICS_SERVICE_URL.rstrip('/')}/analytics/query"
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload.model_dump())
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text or "Analytics service error"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Analytics service unavailable") from exc

    return AnalyticsQueryResponse(**response.json())
