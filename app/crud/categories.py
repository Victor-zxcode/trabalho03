from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    category = Category(name=category_data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.id)))


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_products_for_category(category: Category) -> list[Product]:
    return list(category.products)


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate,
) -> Category:
    for field, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()
