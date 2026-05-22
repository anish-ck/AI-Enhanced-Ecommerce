# Simplified AI Analytics Container Phase

# Objective

Build a simplified AI analytics system for the AI-Enhanced Ecommerce platform.

The system should:

- Use a separate analytics container
- Use Groq API for LLM reasoning
- Query Databricks Gold tables
- Convert natural language to SQL
- Return JSON analytics results
- Generate chart-ready responses
- Render analytics dashboards in React

The architecture should remain simple and practical.

---

# Final Simplified Architecture

```text
React Frontend
      ↓
Main FastAPI Backend
      ↓
Analytics Service Container
      ↓
Groq API (Llama 3.3 70B)
      ↓
Databricks SQL Warehouse
      ↓
Gold Layer Tables
```

---

# Recommended LLM

Use:

```text
llama-3.3-70b-versatile
```

Provider:

```text
Groq API
```

Reason:

- Fast inference
- Excellent SQL generation
- Low latency
- Strong reasoning
- Good free tier
- Ideal for analytics questions

---

# Existing Gold Tables

The AI system must query:

```text
gold.top_products
gold.category_sales
gold.daily_revenue
gold.customer_ltv
gold.monthly_sales
gold.product_performance
```

---

# Create Analytics Container

Create:

```text
analytics_service/
```

---

# Folder Structure

```text
analytics_service/
│
├── app/
│   ├── main.py
│   ├── analytics.py
│   ├── groq_service.py
│   ├── databricks_service.py
│   ├── chart_service.py
│   └── prompts/
│
├── requirements.txt
├── Dockerfile
└── .env
```

---

# Main Flow

```text
User Question
↓
Analytics API
↓
Groq LLM
↓
SQL Generation
↓
Databricks Query
↓
JSON Results
↓
Chart Response
↓
Frontend Dashboard
```

---

# API Endpoint

Create:

```text
POST /analytics/query
```

Request:

```json
{
  "question": "Show top selling products"
}
```

Response:

```json
{
  "question": "Show top selling products",
  "sql": "SELECT * FROM gold.top_products LIMIT 10",
  "chart_type": "bar",
  "data": []
}
```

---

# Phase 1 — Build Basic Analytics API

Start with rule-based query mapping.

Example:

```python
if "top products" in question.lower():
    sql = """
    SELECT *
    FROM gold.top_products
    LIMIT 10
    """
```

Do NOT start with fully autonomous SQL generation.

Keep the first version simple.

---

# Phase 2 — Connect Databricks

Use:

- Databricks SQL Warehouse
- Databricks SQL Connector

Environment Variables:

```env
DATABRICKS_HOST=
DATABRICKS_TOKEN=
DATABRICKS_WAREHOUSE_ID=
```

---

# Phase 3 — Add Groq API

Environment Variables:

```env
GROQ_API_KEY=
```

Recommended Model:

```text
llama-3.3-70b-versatile
```

---

# Groq Prompt Template

```text
You are an AI SQL assistant.

Generate ONLY Databricks SQL.

Available Tables:

gold.top_products
gold.category_sales
gold.daily_revenue
gold.customer_ltv
gold.monthly_sales
gold.product_performance

Rules:
- Return SQL only
- Use valid Databricks SQL
- Never generate DELETE or DROP statements
- Prefer LIMIT 10 for ranking queries
```

---

# Example Analytics Questions

```text
Show top products
Show monthly revenue trend
Which category generated highest revenue?
Show highest lifetime value customers
Show daily revenue
Show best performing products
```

---

# Example Generated SQL

Question:

```text
Show monthly revenue trend
```

Generated SQL:

```sql
SELECT *
FROM gold.monthly_sales
ORDER BY year, month
```

---

# Databricks Query Execution

Responsibilities:

- Execute generated SQL
- Return JSON rows
- Handle errors
- Validate SQL safety

Never directly trust LLM SQL without validation.

---

# Phase 4 — Build Chart Generator

Map analytics results to chart types.

Examples:

| Analytics Type | Chart |
|---|---|
| Revenue Trend | Line Chart |
| Top Products | Bar Chart |
| Category Share | Pie Chart |
| Customer Rankings | Horizontal Bar |

---

# Example Chart Response

```json
{
  "chart_type": "line",
  "x_axis": "month",
  "y_axis": "monthly_revenue"
}
```

---

# Frontend Dashboard

Create:

```text
AnalyticsDashboard.jsx
```

Features:

- Chat input
- Analytics cards
- Charts
- SQL preview
- AI insights
- Tables

---

# Recommended Frontend Libraries

Install:

```bash
npm install recharts axios
```

---

# Recommended Charts

```text
Line Chart
Bar Chart
Pie Chart
Area Chart
```

---

# KPI Cards

Display:

```text
Total Revenue
Top Product
Top Category
Total Orders
Top Customers
```

---

# Docker Setup

Add analytics container.

```yaml
analytics_service:
  build: ./analytics_service
  container_name: analytics_service
  restart: always
  ports:
    - "8001:8001"
  env_file:
    - .env
```

---

# Example End-to-End Flow

Question:

```text
Show top selling products
```

Groq Generates:

```sql
SELECT *
FROM gold.top_products
LIMIT 10
```

Databricks Executes Query.

JSON Returned:

```json
[
  {
    "title": "Gaming Mouse",
    "total_quantity_sold": 500
  }
]
```

Frontend renders:

```text
Bar Chart
```

---

# Recommended Development Order

## Step 1

Create analytics container.

## Step 2

Connect Databricks SQL.

## Step 3

Execute hardcoded SQL queries.

## Step 4

Return JSON results.

## Step 5

Build React dashboard.

## Step 6

Render charts.

## Step 7

Add Groq SQL generation.

## Step 8

Add AI insights.

---

# Important Best Practices

- Keep architecture simple
- Avoid unnecessary microservices
- Validate SQL before execution
- Keep analytics isolated from ecommerce backend
- Use Docker Compose
- Start with hardcoded mappings before dynamic AI SQL

---

# Final Goal

Build a simplified production-style AI analytics platform using:

- React
- FastAPI
- Databricks
- Delta Lake
- Groq API
- Llama 3.3 70B
- Azure Data Lake
- Docker
- AI-powered business analytics

REPLACE WITH MCP-ONLY ARCHITECTURE

Use:

Databricks MCP endpoint

instead of:

SQL Connector
JDBC
Warehouse ID
REQUIRED ENVIRONMENT VARIABLE CHANGES
OLD
DATABRICKS_HOST=
DATABRICKS_TOKEN=
DATABRICKS_WAREHOUSE_ID=
NEW
GROQ_API_KEY=

DATABRICKS_MCP_URL=
DATABRICKS_TOKEN=
REQUIRED MCP URL FORMAT

Example:

https://adb-xxxx.azuredatabricks.net/api/2.0/mcp/sql
REQUIRED ARCHITECTURE CHANGE
OLD FLOW
Frontend
↓
Analytics Service
↓
Databricks SQL Connector
↓
Warehouse
↓
Gold Tables
NEW FLOW
Frontend
↓
Main Backend Proxy
↓
Analytics Container
↓
Groq API
↓
Databricks MCP Endpoint
↓
Gold Tables
REQUIRED LLM CHANGE
OLD

Possible mixed/local models.

NEW

Use ONLY:

Groq API

Recommended model:

llama-3.3-70b-versatile
REQUIRED FOLDER STRUCTURE CHANGE
OLD
databricks_service.py
NEW

Replace with:

mcp_service.py
REQUIRED SERVICE RESPONSIBILITY CHANGE
OLD

databricks_service.py

warehouse connection
JDBC
SQL connector logic
NEW

mcp_service.py

MCP API calls
execute_sql
execute_sql_read_only
poll_sql_result
REQUIRED API FLOW CHANGE
OLD
LLM
↓
SQL Connector
↓
Warehouse
NEW
LLM
↓
MCP execute_sql
↓
Databricks
REQUIRED IMPLEMENTATION SCOPE CHANGE
REMOVE

Do NOT implement:

Redis
Celery
Kubernetes
vector database
RAG
autonomous agents
event-driven architecture
KEEP IMPLEMENTATION SIMPLE

Implement ONLY:

analytics container
Groq integration
MCP integration
SQL generation
JSON response
chart mapping
React dashboard
REQUIRED BACKEND COMMUNICATION CHANGE
OLD

Frontend directly calling analytics container.

NEW

Use backend proxy architecture.

Correct flow:

Frontend
↓
Main FastAPI Backend
↓
Analytics Container

Benefits:

hides internal services
avoids CORS issues
production-style architecture
REQUIRED SQL EXECUTION CHANGE
OLD

Using Databricks SQL connector.

NEW

All SQL execution must happen through MCP endpoint using:

execute_sql
execute_sql_read_only
poll_sql_result
REQUIRED SECURITY CHANGE

Generated SQL must:

allow SELECT only
block DELETE
block UPDATE
block DROP
block ALTER

Validate SQL before MCP execution.

REQUIRED DEVELOPMENT ORDER
Correct order now:
1. Create analytics container
2. Add Docker Compose integration
3. Add MCP connectivity
4. Test hardcoded SQL queries
5. Return JSON results
6. Build React dashboard
7. Add charts
8. Add Groq SQL generation
9. Add AI insights
REQUIRED DOCKER CHANGE

Add ONLY one extra container:

analytics_service:
  build: ./analytics_service
  container_name: analytics_service
  restart: always

  ports:
    - "8001:8001"

  env_file:
    - ./analytics_service/.env

Do NOT add:

multiple analytics services
orchestration layers
distributed containers
FINAL TARGET ARCHITECTURE
React Frontend
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
↓
Charts + Analytics
FINAL IMPLEMENTATION GOAL

Build:

a simplified AI analytics container
Groq-powered SQL generation
MCP-based Databricks querying
React analytics dashboard
chart-ready analytics responses

without unnecessary infrastructure complexity.