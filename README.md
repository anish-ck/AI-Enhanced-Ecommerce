# SignalCart — AI-Powered Ecommerce Analytics Platform

# System Architecture

![System Architecture](assets/architecture.png)

## Overview

SignalCart is a modern AI-enhanced ecommerce and analytics platform that combines:

* AI-powered product content generation
* Intelligent product image understanding
* End-to-end data engineering pipelines
* Medallion architecture (Bronze → Silver → Gold)
* Databricks + Unity Catalog analytics
* LLM-powered conversational analytics
* Dynamic frontend visualizations
* Microservice-based architecture

The platform demonstrates how modern AI systems integrate with data engineering, cloud analytics, and interactive dashboards to create intelligent business intelligence experiences.

---

# Key Features

## Ecommerce Platform

* Product catalog management
* Shopping cart functionality
* Orders management
* Admin dashboard
* Product image uploads
* AI-generated product titles/descriptions/tags

---

## AI Product Intelligence

Using locally hosted LLMs with Ollama:

* AI-generated product titles
* AI-generated descriptions
* AI-generated product tags
* Image-aware product understanding
* Automated ecommerce content enrichment

Example:

```text
Upload Product Image
↓
AI analyzes image
↓
AI generates:
- Product title
- Description
- Tags
- Category suggestions
```

---

## Modern Data Engineering Pipeline

The platform uses a Medallion Architecture:

```text
PostgreSQL
↓
Bronze Layer
↓
Silver Layer
↓
Gold Layer
↓
AI Analytics Engine
```

---

# Architecture

## System Architecture

```text
                        ┌────────────────────┐
                        │   React Frontend   │
                        └─────────┬──────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │ FastAPI Main Backend    │
                    └─────────┬───────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
 ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
 │ PostgreSQL DB  │  │ Ollama LLM     │  │ Analytics API  │
 └────────────────┘  └────────────────┘  └────────┬───────┘
                                                   │
                                                   ▼
                                        ┌──────────────────┐
                                        │ Groq LLM API     │
                                        └────────┬─────────┘
                                                 │
                                                 ▼
                                   ┌─────────────────────────┐
                                   │ Databricks MCP Server   │
                                   └────────┬────────────────┘
                                            │
                                            ▼
                           ┌────────────────────────────────┐
                           │ Unity Catalog Gold Tables      │
                           └────────────────────────────────┘
```

---

# Technology Stack

## Frontend

* React
* Vite
* Tailwind CSS
* Recharts
* Axios

---

## Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL
* Docker

---

## AI & LLM Stack

### Local AI

* Ollama
* Qwen3-VL

### Cloud AI

* Groq API
* Llama Models

---

## Data Engineering Stack

* Databricks
* PySpark
* Delta Lake
* Unity Catalog
* Azure Data Lake Storage Gen2
* Medallion Architecture

---

## Infrastructure

* Docker Compose
* Microservices Architecture
* Azure Cloud Services
* Azure Event Hub
* Apache Kafka-Compatible Streaming

---

## Streaming Architecture

SignalCart also supports event-driven streaming pipelines using:

* Azure Event Hub
* Kafka APIs
* Real-time event ingestion
* Streaming analytics architecture

The platform is designed to support:

```text
Ecommerce Events
↓
Azure Event Hub
↓
Kafka-Compatible Streams
↓
Databricks Structured Streaming
↓
Bronze Streaming Tables
↓
Real-Time Silver Transformations
↓
Live Gold Analytics
```

Potential streaming events:

* order events
* cart activity
* product views
* user activity
* payment events
* inventory updates

This architecture enables:

* real-time analytics
* streaming ETL
* low-latency dashboards
* event-driven systems
* scalable ingestion pipelines
* modern data streaming workflows

---

# Medallion Architecture

## Bronze Layer

Raw ingestion layer.

Stores raw data extracted from PostgreSQL:

* products
* orders
* users
* order_items

Example:

```text
PostgreSQL Tables
↓
Parquet Files in ADLS
↓
Bronze Delta Tables
```

---

## Silver Layer

Cleaned and transformed data.

Transformations include:

* data cleaning
* timestamp conversions
* deduplication
* normalization
* filtering invalid records
* standardization

Example transformations:

* lowercase emails
* cleaned product titles
* valid order filtering
* numeric formatting

---

## Gold Layer

Business-ready analytics layer.

Gold tables:

| Table                    | Purpose                 |
| ------------------------ | ----------------------- |
| gold.top_products        | Best-selling products   |
| gold.monthly_sales       | Monthly revenue trends  |
| gold.customer_ltv        | Customer lifetime value |
| gold.category_sales      | Revenue by category     |
| gold.product_performance | Product analytics       |

---

# AI Analytics Engine

## Conversational Analytics

Users can ask natural language questions such as:

```text
Which product sold most?
```

```text
Show monthly revenue trend
```

```text
Top customers by spending
```

The system automatically:

```text
Question
↓
Groq LLM
↓
SQL Generation
↓
Databricks MCP
↓
Gold Layer Query
↓
JSON Results
↓
Frontend Charts
```

---

# Databricks MCP Integration

SignalCart uses Databricks MCP (Model Context Protocol) to execute AI-generated SQL safely.

Features:

* MCP JSON-RPC communication
* asynchronous query execution
* polling architecture
* typed result parsing
* Unity Catalog integration
* schema-aware SQL generation

---

# Dynamic Analytics Dashboard

The analytics dashboard supports:

* conversational analytics
* dynamic chart rendering
* SQL preview
* raw data visualization
* KPI analytics
* business intelligence workflows

Supported charts:

* line charts
* bar charts
* pie charts

---

# AI Query Pipeline

```text
User Question
↓
Analytics Frontend
↓
Analytics Microservice
↓
Groq LLM
↓
Schema-Aware Prompt
↓
Generated Databricks SQL
↓
Databricks MCP
↓
Gold Layer Tables
↓
Structured Results
↓
Frontend Visualization
```

---

# Dockerized Microservices

The platform uses independent containers for:

| Service            | Purpose                 |
| ------------------ | ----------------------- |
| ecommerce_backend  | Main FastAPI backend    |
| analytics_service  | AI analytics engine     |
| ecommerce_postgres | PostgreSQL database     |
| ecommerce_pgadmin  | Database administration |
| ecommerce_ollama   | Local LLM inference     |

---

# Project Structure

```text
AI-Enhanced-Ecommerce/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   └── services/
│
├── analytics_service/
│   ├── app/
│   ├── prompts/
│   ├── services/
│   └── mcp_service.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── charts/
│
├── databricks/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docker-compose.yml
└── README.md
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd AI-Enhanced-Ecommerce
```

---

## Start Docker Services

```bash
docker compose up --build -d
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Backend

FastAPI backend:

```text
http://localhost:8000
```

Analytics service:

```text
http://localhost:8002
```

Frontend:

```text
http://localhost:5173
```

---

# Example Analytics Questions

```text
Which product sold most?
```

```text
Show monthly revenue trend
```

```text
Top customers by spending
```

```text
Which category generated highest revenue?
```

```text
Compare sales across products
```

---

# Security Features

* schema-aware SQL generation
* restricted SQL operations
* safe MCP execution
* no destructive query support
* prompt constraints
* controlled analytics execution

---

# Future Enhancements

## Planned Features

* real-time streaming analytics
* Kafka integration
* predictive analytics
* recommendation engine
* anomaly detection
* AI forecasting
* multi-tenant analytics
* role-based access control
* vector search
* RAG analytics assistant
* agentic workflows

---

# Learning Outcomes

This project demonstrates practical implementation of:

* AI Engineering
* Data Engineering
* LLM Integration
* Databricks Architecture
* Medallion Architecture
* MCP Protocol
* Cloud Analytics
* Conversational BI
* Full Stack Development
* Docker Microservices
* FastAPI APIs
* React Dashboards

---

# Highlights

## End-to-End AI Analytics Platform

SignalCart is not just an ecommerce application.

It is a complete AI-native analytics ecosystem combining:

* ecommerce workflows
* AI content generation
* cloud data engineering
* Databricks analytics
* conversational BI
* dynamic frontend visualizations
* microservice orchestration

inside a single integrated platform.

---

# Author

Built as an AI-enhanced modern data engineering and analytics platform project integrating:

* Databricks
* FastAPI
* React
* Ollama
* Groq
* MCP
* Delta Lake
* Unity Catalog
* Azure Cloud

---

# License

This project is intended for educational, portfolio, and research purposes.
