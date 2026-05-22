# prompt_changes.md

# Required MCP Result Parsing Changes

The analytics pipeline is now successfully generating SQL using Groq.

Current status:

* FastAPI analytics container works
* Docker setup works
* Groq integration works
* SQL generation works
* MCP connectivity likely works
* chart metadata generation works

However:

```json
"data": []
```

is still empty because MCP query results are not being parsed correctly.

---

# Current Problem

Current response:

```json
{
  "question": "what is monthly sales",
  "sql": "SELECT * FROM gold.monthly_sales ORDER BY year, month",
  "chart_type": "line",
  "data": [],
  "chart": {
    "x_axis": "month",
    "y_axis": "monthly_revenue"
  }
}
```

The SQL generation is now correct.

But the returned query result rows are not being extracted from the MCP response.

---

# Required Changes

# 1. Add MCP Response Logging

Inside:

```text
analytics_service/app/mcp_service.py
```

Add logging immediately after the MCP request.

Current:

```python
response = requests.post(...)
```

Add:

```python
print(response.status_code)
print(response.text)
```

and:

```python
response_json = response.json()
print(response_json)
```

This is required to inspect the exact Databricks MCP response structure.

---

# 2. Replace Empty Data Placeholder

Current implementation likely contains:

```python
"data": []
```

or:

```python
data = []
```

This must be replaced with actual MCP response parsing.

---

# 3. Parse Databricks MCP Result Correctly

The MCP endpoint usually returns:

```json
{
  "result": {
    "data_array": [...]
  }
}
```

OR:

```json
{
  "structuredContent": {
    ...
  }
}
```

The implementation must extract the returned rows.

Example:

```python
response_json = response.json()

rows = response_json["result"]["data_array"]
```

Then return:

```python
return {
    "question": question,
    "sql": sql,
    "chart_type": chart_type,
    "data": rows,
    "chart": chart_config
}
```

---

# 4. Add Safe Parsing Logic

Use safe parsing:

```python
rows = response_json.get("result", {}).get("data_array", [])
```

This prevents crashes if response format changes.

---

# 5. Add MCP Error Logging

Current errors are hidden.

Replace:

```python
except Exception:
    raise HTTPException(
        status_code=502,
        detail="MCP request failed"
    )
```

With:

```python
except Exception as e:
    print("MCP ERROR:", str(e))

    raise HTTPException(
        status_code=502,
        detail=str(e)
    )
```

---

# 6. Preserve Existing Architecture

Keep:

```text
Frontend
↓
Main Backend
↓
Analytics Container
↓
Groq API
↓
Databricks MCP
↓
Gold Tables
```

Do NOT switch back to:

* Databricks SQL connector
* JDBC
* ODBC
* Warehouse ID logic

Continue using MCP-only architecture.

---

# 7. Preserve Existing SQL Prompt Improvements

The schema-aware prompt must remain.

Keep table schemas in:

```text
analytics_service/app/prompts/analytics_prompt.txt
```

Example:

```text
gold.monthly_sales
- year
- month
- monthly_revenue
- total_orders
```

This prevents hallucinated SQL columns.

---

# 8. Expected Final Response

After fixing MCP parsing:

```json
{
  "question": "what is monthly sales",
  "sql": "SELECT * FROM gold.monthly_sales ORDER BY year, month",
  "chart_type": "line",
  "data": [
    {
      "year": 2026,
      "month": 5,
      "monthly_revenue": 50000
    }
  ],
  "chart": {
    "x_axis": "month",
    "y_axis": "monthly_revenue"
  }
}
```

---

# 9. Final Goal

Complete full analytics pipeline:

```text
Question
→ Groq SQL Generation
→ Databricks MCP Query Execution
→ Real Query Results
→ JSON Response
→ Frontend Charts
```

This is the next critical milestone before frontend visualization.


# mcp_result_parsing_changes.md

# Required Changes for MCP Result Parsing

The analytics service is successfully:

* receiving user questions
* generating SQL using Groq
* returning chart metadata
* responding through FastAPI

However:

```json
"data": []
```

is still empty because Databricks MCP query results are not being extracted correctly.

The following exact changes must be implemented.

---

# FILE TO MODIFY

```text
analytics_service/app/mcp_service.py
```

---

# STEP 1 — ADD MCP RESPONSE DEBUG LOGGING

Find:

```python
response = requests.post(
    MCP_URL,
    headers=headers,
    json=payload,
    timeout=60
)
```

Immediately after it, add:

```python
print("MCP STATUS:", response.status_code)
print("MCP RAW RESPONSE:")
print(response.text)
```

Then add:

```python
response_json = response.json()

print("MCP JSON RESPONSE:")
print(response_json)
```

This is required to inspect the actual MCP response structure.

---

# STEP 2 — REMOVE EMPTY DATA PLACEHOLDER

Find any code similar to:

```python
data = []
```

or:

```python
"data": []
```

Remove it.

---

# STEP 3 — PARSE MCP RESPONSE CORRECTLY

Add:

```python
manifest = response_json.get("manifest", {})

columns = manifest.get("schema", {}).get("columns", [])

column_names = [
    col["name"]
    for col in columns
]
```

Then add:

```python
rows = response_json.get("result", {}).get("data_array", [])
```

Then add:

```python
formatted_rows = [
    dict(zip(column_names, row))
    for row in rows
]
```

---

# STEP 4 — RETURN REAL DATA

Replace:

```python
"data": []
```

with:

```python
"data": formatted_rows
```

---

# STEP 5 — ADD SAFE FALLBACKS

Use safe parsing everywhere:

```python
response_json.get(...)
```

Do NOT directly access nested keys without protection.

---

# STEP 6 — ADD BETTER MCP ERROR HANDLING

Find:

```python
except Exception:
    raise HTTPException(
        status_code=502,
        detail="MCP request failed"
    )
```

Replace with:

```python
except Exception as e:
    print("MCP ERROR:", str(e))

    raise HTTPException(
        status_code=502,
        detail=str(e)
    )
```

---

# STEP 7 — VERIFY MCP PAYLOAD FORMAT

Ensure MCP request payload is EXACTLY:

```python
payload = {
    "tool": "execute_sql",
    "arguments": {
        "query": sql
    }
}
```

NOT:

```python
payload = {
    "query": sql
}
```

---

# STEP 8 — VERIFY MCP URL

Ensure:

```env
DATABRICKS_MCP_URL=https://adb-xxxx.azuredatabricks.net/api/2.0/mcp/sql
```

NOT:

```env
/api/2.0/sql/warehouses
```

---

# STEP 9 — EXPECTED FINAL RESPONSE

After fixes:

```json
{
  "question": "which product sold most?",
  "sql": "SELECT title FROM gold.top_products ORDER BY total_quantity_sold DESC LIMIT 1",
  "chart_type": "bar",
  "data": [
    {
      "title": "Gaming Mouse"
    }
  ],
  "chart": {
    "x_axis": "title",
    "y_axis": "total_quantity_sold"
  }
}
```

---

# STEP 10 — REBUILD CONTAINERS

After code changes:

```bash
docker compose down
docker compose up --build -d
```

---

# STEP 11 — VERIFY LOGS

Run:

```bash
docker logs -f analytics_service
```

Then test API again.

The logs should now display:

* MCP raw response
* parsed rows
* formatted output
* real analytics data

---

# FINAL GOAL

Complete full analytics execution pipeline:

```text
Question
→ Groq SQL Generation
→ Databricks MCP Query Execution
→ MCP Result Parsing
→ JSON Analytics Response
→ Frontend Charts
```
