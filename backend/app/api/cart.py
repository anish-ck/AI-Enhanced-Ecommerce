from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import get_db
from app.events.producer import publish_event
from app.events.schemas import AddToCartEvent
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemOut, CartItemUpdate

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=list[CartItemOut])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CartItem]:
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .order_by(CartItem.id)
        .all()
    )


@router.post("/add", response_model=CartItemOut)
def add_to_cart(
    payload: CartItemCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartItem:
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == payload.product_id,
        )
        .first()
    )
    if cart_item:
        cart_item.quantity += payload.quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    event = AddToCartEvent(
        user_id=current_user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
    )
    background_tasks.add_task(publish_event, event)
    return cart_item


@router.put("/update", response_model=CartItemOut)
def update_cart_item(
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartItem:
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == payload.product_id,
        )
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = payload.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/remove", response_model=None)
def remove_from_cart(
    product_id: int = Query(..., description="Product ID to remove"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id,
        )
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return None
