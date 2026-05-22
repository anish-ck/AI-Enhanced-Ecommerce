from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user_optional
from app.db.database import get_db
from app.events.producer import publish_event
from app.events.schemas import ProductViewEvent
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.schemas.ai import AIGenerateResult
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.ollama import OllamaError, generate_product_content

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return db.query(Product).order_by(Product.id).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if current_user:
        event = ProductViewEvent(user_id=current_user.id, product_id=product.id)
        background_tasks.add_task(publish_event, event)
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
) -> Product:
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    product = Product(
        title=payload.title,
        description=payload.description,
        category_id=payload.category_id,
        price=payload.price,
        stock=payload.stock,
        ai_title=payload.ai_title,
        ai_description=payload.ai_description,
        ai_category=payload.ai_category,
        ai_tags=payload.ai_tags,
        ai_generated=payload.ai_generated if payload.ai_generated is not None else False,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.post("/ai-generate", response_model=AIGenerateResult)
async def generate_ai_content(
    image: UploadFile = File(...),
    product_id: int | None = Form(default=None),
    db: Session = Depends(get_db),
) -> AIGenerateResult:
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Image is required")

    try:
        generated = generate_product_content(image_bytes)
    except OllamaError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if product_id is not None:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.ai_title = generated.ai_title
        product.ai_description = generated.ai_description
        product.ai_category = generated.ai_category
        product.ai_tags = generated.ai_tags
        product.ai_generated = True
        db.commit()

    return AIGenerateResult(
        ai_title=generated.ai_title,
        ai_description=generated.ai_description,
        ai_category=generated.ai_category,
        ai_tags=generated.ai_tags,
        product_id=product_id,
    )


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return None
