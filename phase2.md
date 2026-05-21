You are helping build an AI-enhanced ecommerce platform using:

* FastAPI backend
* PostgreSQL
* Docker
* Azure Event Hub (Kafka-compatible endpoint)
* React frontend

Current backend already supports:

* authentication
* products
* cart
* orders
* PostgreSQL integration

Current database already contains:

* products
* users
* orders
* order_items

Goal:
Integrate Azure Event Hub streaming into the FastAPI backend using kafka-python.

Requirements:

1. Create a new folder:

app/events/

2. Create:

* producer.py
* consumer.py
* schemas.py

3. Use kafka-python to connect to Azure Event Hub Kafka endpoint.

4. Read Event Hub connection details from environment variables.

Required environment variables:

EVENT_HUB_BOOTSTRAP_SERVER=
EVENT_HUB_CONNECTION_STRING=
EVENT_HUB_TOPIC=

5. Implement a reusable Kafka producer.

6. Producer must:

* serialize JSON safely
* include timestamps
* handle failures gracefully
* never break APIs if Event Hub fails

Use:
try/except logging

7. Define event schemas for:

* product_view
* add_to_cart
* checkout_completed

8. Integrate events into existing FastAPI routes.

Required integrations:

GET /products/{id}
→ emit product_view event

POST /cart/add
→ emit add_to_cart event

POST /orders/create
→ emit checkout_completed event

9. Event payload examples:

product_view:
{
"event_type": "product_view",
"user_id": 1,
"product_id": 55,
"timestamp": "ISO_TIMESTAMP"
}

add_to_cart:
{
"event_type": "add_to_cart",
"user_id": 1,
"product_id": 55,
"quantity": 2,
"timestamp": "ISO_TIMESTAMP"
}

checkout_completed:
{
"event_type": "checkout_completed",
"user_id": 1,
"order_id": 101,
"total_amount": 199.99,
"timestamp": "ISO_TIMESTAMP"
}

10. Create a simple local consumer in consumer.py that:

* connects to Event Hub
* continuously reads events
* prints received events

11. Add proper logging for:

* successful event publishing
* failures
* retries

12. Maintain clean architecture:

* business logic separate from event logic
* reusable event producer service
* modular design

13. Do NOT change existing database schema.

14. Do NOT implement Databricks, Spark, or ADF yet.

15. Ensure code is production-style and scalable for future streaming pipelines.

Generate:

* all required Python files
* environment variable usage
* integration examples
* dependency requirements
* folder structure updates
* reusable helper functions
* clean code comments
