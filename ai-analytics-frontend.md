# analytics_frontend_prompt.md

# Objective

Build a modern AI Analytics Dashboard frontend for the AI-Enhanced-Ecommerce project.

The frontend must connect to the existing analytics microservice API and dynamically visualize analytics results returned from the backend.

The backend is already fully working.

Current architecture:

```text id="1j2w9e"
Frontend
↓
FastAPI Backend
↓
Analytics Service
↓
Groq LLM
↓
Databricks MCP
↓
Gold Layer Tables
↓
JSON Analytics Results
```

The frontend task is ONLY visualization and interaction.

---

# Existing Analytics API

Analytics endpoint:

```text id="q5k8vm"
POST http://localhost:8002/analytics/query
```

Request body:

```json id="s7v4ta"
{
  "question": "Which product sold most?"
}
```

Example response:

```json id="f3n8qx"
{
  "question": "Which product sold most?",
  "sql": "SELECT title FROM gold.top_products ORDER BY total_quantity_sold DESC LIMIT 1",
  "chart_type": "bar",
  "data": [
    {
      "title": "PAPER CRAFT , LITTLE BIRDIE"
    }
  ],
  "chart": {
    "x_axis": "title",
    "y_axis": "total_quantity_sold"
  }
}
```

---

# Frontend Requirements

Build a complete analytics dashboard page using React.

Preferred stack:

* React
* Vite
* Tailwind CSS
* Recharts
* Axios

---

# Required Features

# 1. Analytics Dashboard Page

Create:

```text id="g2r9xy"
/analytics
```

Page must contain:

* AI analytics search box
* submit button
* loading state
* error handling
* chart visualization area
* SQL preview area
* raw data table

---

# 2. User Question Input

User should type questions like:

```text id="d8m1pw"
Which product sold most?
```

```text id="v4k7rt"
Show monthly revenue trend
```

```text id="m6n2qy"
Top customers by spending
```

---

# 3. Call Analytics API

Use Axios.

Example:

```javascript id="w9f3eu"
axios.post("http://localhost:8002/analytics/query", {
  question: userQuestion
})
```

---

# 4. Dynamic Chart Rendering

Render charts dynamically based on:

```json id="u1p8zc"
chart_type
```

Supported charts:

* bar
* line
* pie

Use Recharts.

---

# 5. Dynamic Axis Mapping

Use:

```json id="k7d2ax"
chart.x_axis
chart.y_axis
```

for chart configuration.

Do NOT hardcode axes.

---

# 6. Raw SQL Display

Display generated SQL query inside a styled card.

Example:

```sql id="y4m9tb"
SELECT title
FROM gold.top_products
ORDER BY total_quantity_sold DESC
LIMIT 1
```

---

# 7. Raw Data Table

Render backend data as a table.

Columns should generate dynamically from JSON keys.

---

# 8. Loading State

Show:

```text id="c5n7wu"
Generating analytics...
```

while waiting for API response.

---

# 9. Error Handling

Display backend errors gracefully.

Example:

```text id="t1x8ro"
Failed to generate analytics
```

---

# 10. Dashboard Styling

Use modern dark dashboard styling.

Requirements:

* glassmorphism cards
* rounded corners
* responsive layout
* modern analytics UI
* clean spacing
* gradient buttons
* dark background

---

# 11. Suggested Layout

```text id="b2q4ks"
------------------------------------------------
| AI Analytics Dashboard                       |
------------------------------------------------
| Ask a business question... [Generate]        |
------------------------------------------------
| Chart Visualization                          |
------------------------------------------------
| Generated SQL                                |
------------------------------------------------
| Raw Data Table                               |
------------------------------------------------
```

---

# 12. Component Structure

Suggested structure:

```text id="e7v1dp"
src/
 ├── pages/
 │    └── AnalyticsPage.jsx
 │
 ├── components/
 │    ├── AnalyticsInput.jsx
 │    ├── AnalyticsChart.jsx
 │    ├── SQLPreview.jsx
 │    ├── DataTable.jsx
 │    └── LoadingSpinner.jsx
```

---

# 13. AnalyticsChart Component

Must dynamically switch charts.

Example:

```javascript id="h3k8mu"
if (chartType === "bar") {
   return <BarChart ... />
}
```

---

# 14. DataTable Component

Generate columns dynamically:

```javascript id="p8n4ws"
Object.keys(data[0])
```

---

# 15. SQL Preview Styling

Use monospace font.

Dark code editor style.

---

# 16. Important Constraints

Do NOT:

* hardcode product fields
* hardcode chart axes
* hardcode table columns
* hardcode chart types

Everything must be dynamic from backend response.

---

# 17. Expected Final Flow

```text id="x5m9ka"
User Question
↓
Frontend API Call
↓
Analytics Service
↓
Groq SQL Generation
↓
Databricks MCP
↓
Gold Layer Query
↓
JSON Analytics Result
↓
Dynamic Frontend Visualization
```

---

# 18. Deliverables

Generate:

* complete React frontend code
* Tailwind styling
* Recharts integration
* Axios integration
* reusable components
* responsive analytics dashboard

---

# 19. Final Goal

The frontend should behave like:

* Power BI AI assistant
* Tableau AI analytics
* Databricks Genie
* conversational analytics dashboard

using the already working AI analytics backend.


fastapi_cors_fix.md
Problem

Frontend requests are failing with:

OPTIONS /analytics/query HTTP/1.1" 405 Method Not Allowed

This happens because browsers send:

CORS preflight OPTIONS requests

before POST requests.

FastAPI currently does not allow CORS.

FILE TO MODIFY
analytics_service/app/main.py
STEP 1 — IMPORT CORSMiddleware

Add:

from fastapi.middleware.cors import CORSMiddleware
STEP 2 — ADD CORS MIDDLEWARE

Immediately after:

app = FastAPI()

Add:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
IMPORTANT

This enables:

OPTIONS requests
frontend API calls
React frontend communication
STEP 3 — REBUILD CONTAINERS

Run:

docker compose down
docker compose up --build -d
STEP 4 — VERIFY

After restart:

Frontend requests should succeed.

Logs should show:

OPTIONS /analytics/query HTTP/1.1" 200 OK

instead of:

405 Method Not Allowed