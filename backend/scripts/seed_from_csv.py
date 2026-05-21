import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.models import Category, Order, OrderItem, Product, Review, User

BASE_DIR = Path(__file__).resolve().parent.parent
REVIEWS_PATH = BASE_DIR / "data" / "reviews_sample.csv"
TRANSACTIONS_PATH = BASE_DIR / "data" / "transactions_sample.csv"


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()

    value = value.strip()
    for fmt in (
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return datetime.utcnow()


def to_decimal(value: str | None, default: Decimal = Decimal("0")) -> Decimal:
    if value is None:
        return default
    try:
        return Decimal(str(value).strip())
    except Exception:
        return default


def to_int(value: str | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def get_or_create_category(session, name: str, cache: dict[str, Category]) -> Category:
    name = name.strip() or "Uncategorized"
    if name in cache:
        return cache[name]

    category = session.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name)
        session.add(category)
        session.flush()
    cache[name] = category
    return category


def get_or_create_user(session, email: str, name: str, cache: dict[str, User], password_hash: str) -> User:
    if email in cache:
        return cache[email]

    user = session.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, password_hash=password_hash)
        session.add(user)
        session.flush()
    cache[email] = user
    return user


def seed_reviews(session) -> int:
    if not REVIEWS_PATH.exists():
        raise FileNotFoundError(f"Missing reviews sample at {REVIEWS_PATH}")

    category_cache: dict[str, Category] = {}

    products_existing = {p.id for p in session.query(Product.id).all()}
    categories_existing = {c.name: c for c in session.query(Category).all()}
    category_cache.update(categories_existing)

    products_to_create: dict[int, dict[str, str]] = {}

    with open(REVIEWS_PATH, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                product_id = int(row.get("product_id", "0"))
            except ValueError:
                continue
            if product_id <= 0:
                continue

            if product_id not in products_existing and product_id not in products_to_create:
                title = (row.get("product_title") or "").strip() or f"Product {product_id}"
                category_name = (row.get("category") or "Uncategorized").strip() or "Uncategorized"
                products_to_create[product_id] = {
                    "title": title,
                    "category": category_name,
                }

    for product_id, info in products_to_create.items():
        category = get_or_create_category(session, info["category"], category_cache)
        product = Product(
            id=product_id,
            title=info["title"],
            description=info["title"],
            category_id=category.id,
            price=Decimal("19.99"),
            stock=100,
        )
        session.add(product)

    session.commit()

    review_password = hash_password("Review@123")
    reviewer = get_or_create_user(
        session,
        email="reviewer@seed.local",
        name="Seed Reviewer",
        cache={},
        password_hash=review_password,
    )

    reviews_created = 0
    batch = []
    batch_size = 2000

    with open(REVIEWS_PATH, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                product_id = int(row.get("product_id", "0"))
            except ValueError:
                continue
            if product_id <= 0:
                continue

            rating = to_int(row.get("rating"), default=5)
            rating = max(1, min(5, rating))
            review_text = (row.get("review_text") or "").strip() or "Seed review"

            batch.append(
                Review(
                    product_id=product_id,
                    user_id=reviewer.id,
                    rating=rating,
                    review_text=review_text,
                )
            )
            reviews_created += 1

            if len(batch) >= batch_size:
                session.add_all(batch)
                session.flush()
                batch.clear()

    if batch:
        session.add_all(batch)
        session.flush()

    session.commit()
    return reviews_created


def seed_transactions(session) -> tuple[int, int, int]:
    if not TRANSACTIONS_PATH.exists():
        raise FileNotFoundError(f"Missing transactions sample at {TRANSACTIONS_PATH}")

    category_cache: dict[str, Category] = {}
    categories_existing = {c.name: c for c in session.query(Category).all()}
    category_cache.update(categories_existing)
    sales_category = get_or_create_category(session, "Imported Sales", category_cache)

    max_product_id = session.query(Product.id).order_by(Product.id.desc()).limit(1).scalar() or 0
    next_product_id = max_product_id + 1

    product_map: dict[str, int] = {}
    user_cache: dict[str, User] = {}
    order_map: dict[str, Order] = {}
    order_totals: dict[str, Decimal] = {}

    default_password_hash = hash_password("Seed@123")

    order_items_batch = []
    order_items_count = 0
    batch_size = 5000

    with open(TRANSACTIONS_PATH, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            invoice_no = (row.get("InvoiceNo") or "").strip()
            stock_code = (row.get("StockCode") or "").strip()
            description = (row.get("Description") or "").strip() or f"Item {stock_code}"
            quantity = to_int(row.get("Quantity"), default=0)
            unit_price = to_decimal(row.get("UnitPrice"))

            if not invoice_no or not stock_code:
                continue
            if quantity <= 0 or unit_price <= 0:
                continue

            if stock_code not in product_map:
                product_id = next_product_id
                next_product_id += 1
                product = Product(
                    id=product_id,
                    title=description,
                    description=description,
                    category_id=sales_category.id,
                    price=unit_price,
                    stock=500,
                )
                session.add(product)
                product_map[stock_code] = product_id

            customer_id = (row.get("CustomerID") or "").strip() or "guest"
            email = (
                f"customer_{customer_id}@seed.local"
                if customer_id != "guest"
                else "guest@seed.local"
            )
            name = (
                f"Customer {customer_id}"
                if customer_id != "guest"
                else "Guest Customer"
            )
            user = get_or_create_user(
                session,
                email=email,
                name=name,
                cache=user_cache,
                password_hash=default_password_hash,
            )

            if invoice_no not in order_map:
                order = Order(
                    user_id=user.id,
                    total_amount=Decimal("0"),
                    status="completed",
                    created_at=parse_datetime(row.get("InvoiceDate")),
                )
                session.add(order)
                session.flush()
                order_map[invoice_no] = order
                order_totals[invoice_no] = Decimal("0")

            order = order_map[invoice_no]
            order_total = order_totals[invoice_no]
            order_total += unit_price * Decimal(quantity)
            order_totals[invoice_no] = order_total

            order_items_batch.append(
                OrderItem(
                    order_id=order.id,
                    product_id=product_map[stock_code],
                    quantity=quantity,
                    price=unit_price,
                )
            )
            order_items_count += 1

            if len(order_items_batch) >= batch_size:
                session.add_all(order_items_batch)
                session.flush()
                order_items_batch.clear()

    if order_items_batch:
        session.add_all(order_items_batch)
        session.flush()

    for invoice_no, order in order_map.items():
        order.total_amount = order_totals[invoice_no]

    session.commit()
    return len(product_map), len(order_map), order_items_count


def main() -> None:
    init_db()
    session = SessionLocal()

    try:
        print("Seeding reviews...")
        reviews_count = seed_reviews(session)
        print(f"Reviews created: {reviews_count}")

        print("Seeding transactions...")
        products_count, orders_count, items_count = seed_transactions(session)
        print(f"Products added from transactions: {products_count}")
        print(f"Orders created: {orders_count}")
        print(f"Order items created: {items_count}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
