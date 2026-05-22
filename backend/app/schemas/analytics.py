from pydantic import BaseModel, Field


class AnalyticsQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class ChartInfo(BaseModel):
    x_axis: str | None = None
    y_axis: str | None = None


class AnalyticsQueryResponse(BaseModel):
    question: str
    sql: str
    chart_type: str
    data: list[dict]
    chart: ChartInfo | None = None
