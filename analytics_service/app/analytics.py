from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.chart_service import infer_chart
from app.mcp_service import MCPError, execute_sql_read_only
from app.groq_service import GroqError, generate_sql
from app.schemas import AnalyticsQueryRequest, AnalyticsQueryResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

RULES: list[tuple[list[str], str]] = [
    (
        ["top products", "top selling", "best products"],
        "SELECT * FROM gold.top_products LIMIT 10",
    ),
    (
        ["category", "highest revenue", "category revenue", "category sales"],
        "SELECT * FROM gold.category_sales ORDER BY total_revenue DESC LIMIT 10",
    ),
    (
        ["daily revenue", "daily sales"],
        "SELECT * FROM gold.daily_revenue ORDER BY date",
    ),
    (
        ["monthly revenue", "monthly sales", "monthly trend"],
        "SELECT * FROM gold.monthly_sales ORDER BY year, month",
    ),
    (
        ["lifetime value", "ltv", "top customers", "highest value customers"],
        "SELECT * FROM gold.customer_ltv ORDER BY lifetime_value DESC LIMIT 10",
    ),
    (
        ["product performance", "best performing products", "performance"],
        "SELECT * FROM gold.product_performance ORDER BY performance_score DESC LIMIT 10",
    ),
]

FORBIDDEN_SQL = [
    "delete",
    "drop",
    "update",
    "insert",
    "alter",
    "create",
    "truncate",
    "merge",
]


def _map_question_to_sql(question: str) -> str | None:
    lowered = question.lower()
    for triggers, sql in RULES:
        if any(trigger in lowered for trigger in triggers):
            return sql
    return None


def _is_sql_safe(sql: str) -> bool:
    lowered = sql.strip().lower()
    if not lowered.startswith(("select", "with")):
        return False
    return not any(keyword in lowered for keyword in FORBIDDEN_SQL)


@router.post("/query", response_model=AnalyticsQueryResponse)
def analytics_query(payload: AnalyticsQueryRequest) -> AnalyticsQueryResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    sql = _map_question_to_sql(question)
    if sql is None:
        try:
            sql = generate_sql(question)
        except GroqError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not sql or not _is_sql_safe(sql):
        raise HTTPException(status_code=400, detail="Generated SQL failed safety checks")

    try:
        rows = execute_sql_read_only(sql)
    except MCPError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        print("MCP ERROR:", str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    chart_type, chart = infer_chart(question, sql)

    return AnalyticsQueryResponse(
        question=question,
        sql=sql,
        chart_type=chart_type,
        chart=chart,
        data=jsonable_encoder(rows),
    )
