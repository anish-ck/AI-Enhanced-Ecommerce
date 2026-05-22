# Phase 1 — AI Commerce Platform (Core OLTP System)

# Objective

Build the foundational transactional e-commerce platform before moving into:

- Azure Event Hub
- Databricks
- Delta Lake
- RAG
- MCP
- AI Analytics

This phase establishes the:

# OLTP (Online Transaction Processing) Layer

---

# Final Phase 1 Architecture

```text
React + Vite
      ↓
FastAPI
      ↓
PostgreSQL
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Containers | Docker |
| API Testing | Postman |
| OS | Ubuntu Linux |

---

# Phase 1 Deliverables

By the end of Phase 1, the system should include:

✅ User authentication
✅ Product management
✅ Category management
✅ Cart system
✅ Order system
✅ Review system
✅ Dockerized PostgreSQL
✅ FastAPI backend
✅ React frontend
✅ API documentation

---

# Step 1 — Install Required Tools (Ubuntu)

## Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

Enable Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Add user permissions:

```bash
sudo usermod -aG docker $USER
```

Reboot:

```bash
reboot
```

Verify:

```bash
docker --version
```

---

## Install Docker Compose

```bash
docker compose version
```

---

## Install Python Tools

```bash
sudo apt install python3-pip python3-venv -y
```

Verify:

```bash
python3 --version
```

---

## Install Node.js

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify:

```bash
node -v
npm -v
```

---

## Install PostgreSQL Client

```bash
sudo apt install postgresql-client -y
```

---

# Step 2 — Create Project Structure


in this folder


---

# Step 3 — Setup Frontend

## Create React + Vite App

```bash
npm create vite@latest frontend
```

Choose:

```text
React
JavaScript
```

---

## Install Dependencies

```bash
cd frontend
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Step 4 — Setup Backend

Go back:

```bash
cd ..
mkdir backend
cd backend
```

---

## Create Python Virtual Environment

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## Install FastAPI Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-dotenv pydantic email-validator
```

Save requirements:

```bash
pip freeze > requirements.txt
```

---

# Step 5 — Backend Folder Structure

Inside backend:

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
├── .env
└── Dockerfile
```

Create folders:

```bash
mkdir -p app/api
mkdir -p app/core
mkdir -p app/db
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/services
```

---

# Step 6 — Setup PostgreSQL with Docker

Go to project root:

```bash
cd ..
```

Create:

```text
docker-compose.yml
```

---

# docker-compose.yml

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16
    container_name: ecommerce_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ecommerce_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    container_name: ecommerce_pgadmin
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"

volumes:
  postgres_data:
```

---

# Start PostgreSQL

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

# pgAdmin Access

```text
http://localhost:5050
```

Credentials:

```text
Email: admin@example.com
Password: admin
```

---

# Step 7 — Database Schema Design

# Core Tables

## users

| Column | Type |
|---|---|
| id | UUID/int |
| name | text |
| email | text |
| password_hash | text |
| created_at | timestamp |

---

## categories

| Column | Type |
|---|---|
| id | int |
| name | text |

---

## products

| Column | Type |
|---|---|
| id | int |
| title | text |
| description | text |
| category_id | int |
| price | decimal |
| stock | int |
| created_at | timestamp |

---

## cart_items

| Column | Type |
|---|---|
| id | int |
| user_id | int |
| product_id | int |
| quantity | int |

---

## orders

| Column | Type |
|---|---|
| id | int |
| user_id | int |
| total_amount | decimal |
| status | text |
| created_at | timestamp |

---

## order_items

| Column | Type |
|---|---|
| id | int |
| order_id | int |
| product_id | int |
| quantity | int |
| price | decimal |

---

## reviews

| Column | Type |
|---|---|
| id | int |
| product_id | int |
| user_id | int |
| rating | int |
| review_text | text |
| created_at | timestamp |

---

# Why Reviews Matter

These will later be used for:

- RAG
- embeddings
- semantic search
- review summarization
- recommendation systems

---

# Step 8 — Setup Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_db
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Step 9 — Setup Database Connection

Create:

```text
backend/app/db/database.py
```

Responsibilities:

- SQLAlchemy engine
- SessionLocal
- Base class
- database connection

---

# Step 10 — Create SQLAlchemy Models

Create model files:

```text
models/user.py
models/product.py
models/category.py
models/cart.py
models/order.py
models/review.py
```

---

# Relationships to Implement

| Table | Relationship |
|---|---|
| User → Orders | one-to-many |
| Product → Reviews | one-to-many |
| Category → Products | one-to-many |
| Order → OrderItems | one-to-many |

---

# Step 11 — JWT Authentication

# Features

Implement:

✅ Signup
✅ Login
✅ Password hashing
✅ JWT token generation
✅ Protected routes

---

# Recommended Auth Endpoints

```text
POST /auth/signup
POST /auth/login
GET /auth/me
```

---

# Step 12 — Product APIs

# Features

✅ Create product
✅ Update product
✅ Delete product
✅ List products
✅ Product details

---

# Product Endpoints

```text
GET /products
GET /products/{id}
POST /products
PUT /products/{id}
DELETE /products/{id}
```

---

# Step 13 — Category APIs

```text
GET /categories
POST /categories
```

---

# Step 14 — Cart APIs

# Features

✅ Add item
✅ Remove item
✅ Update quantity
✅ View cart

---

# Cart Endpoints

```text
POST /cart/add
DELETE /cart/remove
PUT /cart/update
GET /cart
```

---

# Step 15 — Order APIs

# Features

✅ Checkout
✅ Create order
✅ View orders
✅ View order history

---

# Order Endpoints

```text
POST /orders/create
GET /orders
GET /orders/{id}
```

---

# Step 16 — Review APIs

# Features

✅ Add review
✅ View reviews

---

# Review Endpoints

```text
POST /reviews
GET /products/{id}/reviews
```

---

# Step 17 — API Documentation

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# Step 18 — Frontend Pages

# Minimum Pages

## Authentication

- Login page
- Signup page

---

## Product Pages

- Product listing
- Product details

---

## Cart Pages

- Cart page
- Checkout page

---

## Orders

- Order history

---

# Step 19 — Frontend Features

# Required Features

✅ Fetch products from API
✅ JWT login handling
✅ Store token
✅ Add to cart
✅ Checkout flow
✅ Submit reviews

---

# Step 20 — API Testing

Use:

- Postman
- Swagger Docs

Test:

✅ Authentication
✅ CRUD APIs
✅ Cart operations
✅ Orders
✅ Reviews

---

# Step 21 — Git Setup

Initialize git:

```bash
git init
```

Create:

```text
.gitignore
```

Add:

```text
venv/
node_modules/
.env
__pycache__/
```

---

# Step 22 — Dockerize Backend (Optional in Phase 1)

Later you can containerize FastAPI.

For now:

✅ PostgreSQL in Docker
✅ FastAPI local
✅ React local

is enough.

---

# Important Development Principles

# Keep Phase 1 Simple

Do NOT add yet:

❌ Event Hub
❌ Databricks
❌ Delta Lake
❌ AI pipelines
❌ RAG
❌ MCP
❌ Vector DB

---

# Why Phase 1 Matters

This phase creates the:

# Source Operational Database

Later phases depend on:

- products
- orders
- reviews
- users
- events

Without a clean OLTP system, your analytics architecture becomes messy.

---

# What Later Phases Will Use

| Table | Future Usage |
|---|---|
| orders | sales analytics |
| reviews | RAG + embeddings |
| products | semantic search |
| users | personalization |

---

# Phase 1 Final Checklist

# Infrastructure

✅ Docker PostgreSQL
✅ pgAdmin
✅ Backend structure
✅ Frontend structure

---

# Backend

✅ FastAPI
✅ SQLAlchemy
✅ JWT auth
✅ CRUD APIs

---

# Database

✅ PostgreSQL schema
✅ relationships
✅ indexes

---

# Frontend

✅ Login/signup
✅ Product pages
✅ Cart system
✅ Orders

---

# API Layer

✅ Swagger docs
✅ Tested endpoints

---

# After Phase 1

Next phase:

# Phase 2 — Event Streaming Architecture

Where you will add:

- Azure Event Hub
- Kafka architecture
- eve