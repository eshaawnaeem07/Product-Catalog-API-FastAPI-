from sqlalchemy.orm import Session
from app.models.product import Product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, category_id: int | None = None):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()

def create_product(db: Session, obj):
    db_obj = Product(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_product(db: Session, db_obj, obj):
    for field, value in obj.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_product(db: Session, db_obj):
    db.delete(db_obj)
    db.commit()