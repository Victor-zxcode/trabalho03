from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(
        name=product_data.name,
        category_id=product_data.category_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.id)))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:
    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def category_exists(db: Session, category_id: int) -> bool:
    return db.get(Category, category_id) is not None


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
