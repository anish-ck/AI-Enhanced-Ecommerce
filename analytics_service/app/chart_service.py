import re

from app.schemas import ChartInfo

TABLE_CHARTS: dict[str, tuple[str, ChartInfo | None]] = {
    "gold.top_products": ("bar", ChartInfo(x_axis="title", y_axis="total_quantity_sold")),
    "gold.category_sales": ("pie", ChartInfo(x_axis="category", y_axis="total_revenue")),
    "gold.daily_revenue": ("line", ChartInfo(x_axis="date", y_axis="daily_revenue")),
    "gold.customer_ltv": ("bar", ChartInfo(x_axis="customer", y_axis="lifetime_value")),
    "gold.monthly_sales": ("line", ChartInfo(x_axis="month", y_axis="monthly_revenue")),
    "gold.product_performance": ("bar", ChartInfo(x_axis="product", y_axis="performance_score")),
}


def _extract_table(sql: str) -> str | None:
    match = re.search(r"(gold\.[a-z_]+)", sql.lower())
    if match:
        return match.group(1)
    return None


def infer_chart(question: str, sql: str) -> tuple[str, ChartInfo | None]:
    table = _extract_table(sql)
    if table and table in TABLE_CHARTS:
        return TABLE_CHARTS[table]

    lowered = question.lower()
    if "trend" in lowered or "daily" in lowered or "monthly" in lowered:
        return "line", ChartInfo(x_axis="time", y_axis="value")
    if "category" in lowered:
        return "pie", ChartInfo(x_axis="category", y_axis="value")
    if "top" in lowered or "best" in lowered:
        return "bar", ChartInfo(x_axis="item", y_axis="value")

    return "table", None
