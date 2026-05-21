import argparse

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.models import Order, User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create demo user and attach orders")
    parser.add_argument("--email", default="demo@example.com")
    parser.add_argument("--name", default="Demo User")
    parser.add_argument("--password", default="Demo@123")
    parser.add_argument("--orders", type=int, default=20)

    args = parser.parse_args()

    init_db()
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == args.email).first()
        if not user:
            user = User(
                name=args.name,
                email=args.email,
                password_hash=hash_password(args.password),
            )
            session.add(user)
            session.flush()
        else:
            user.name = args.name
            user.password_hash = hash_password(args.password)

        orders = (
            session.query(Order)
            .order_by(Order.created_at.desc())
            .limit(args.orders)
            .all()
        )

        for order in orders:
            order.user_id = user.id

        session.commit()
        print(f"Demo user: {user.email}")
        print(f"Orders assigned: {len(orders)}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
