from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.api.routes.auth import get_current_user
from app.models.user import User
from typing import List
from app.cache import get_cache, set_cache, delete_cache

# # Category routes for CRUD operations on product categories
# router = APIRouter(prefix="/categories", tags=["Categories"])

# # Get all categories or filter by category_id
# @router.get("/", response_model=List[CategoryOut])
# def get_categories(db: Session = Depends(get_db)):
#     categories = db.query(Category).all()
#     return categories

# # Get a single category by ID
# @router.get("/{id}", response_model=CategoryOut)
# def get_category(id: int, db: Session = Depends(get_db)):
#     category = db.query(Category).filter(Category.id == id).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category

# # Create a new category (requires authentication)
# @router.post("/", response_model=CategoryOut)
# def create_category(
#     category: CategoryCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     new_category = Category(**category.dict())
#     db.add(new_category)
#     db.commit()
#     db.refresh(new_category)
#     return new_category

# # Update an existing category (requires authentication)
# @router.put("/{id}", response_model=CategoryOut)
# def update_category(
#     id: int,
#     category: CategoryUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_category = db.query(Category).filter(Category.id == id).first()

#     if not db_category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     for key, value in category.dict(exclude_unset=True).items():
#         setattr(db_category, key, value)

#     db.commit()
#     db.refresh(db_category)
#     return db_category

# # Delete a category (requires authentication)
# @router.delete("/{id}")
# def delete_category(
#     id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     category = db.query(Category).filter(Category.id == id).first()

#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     db.delete(category)
#     db.commit()

#     return {"message": "Category deleted"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.api.routes.auth import get_current_user
from app.models.user import User
from typing import List
from app.cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/categories", tags=["Categories"])


# Get all categories
@router.get("/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):

    cache_key = "categories:all"

    cached = get_cache(cache_key)
    if cached:
        return cached

    categories = db.query(Category).all()

    result = [CategoryOut.model_validate(c).model_dump() for c in categories]

    set_cache(cache_key, result, expire=120)

    return result


# Get single category
@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):

    cache_key = f"category:{id}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    result = CategoryOut.model_validate(category).model_dump()

    set_cache(cache_key, result, expire=120)

    return result


# Create category
@router.post("/", response_model=CategoryOut)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_category = Category(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    delete_cache("categories:all")  # invalidate list cache

    return new_category


# Update category
@router.put("/{id}", response_model=CategoryOut)
def update_category(
    id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_category = db.query(Category).filter(Category.id == id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    delete_cache(f"category:{id}")
    delete_cache("categories:all")

    return db_category


# Delete category
@router.delete("/{id}")
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    delete_cache(f"category:{id}")
    delete_cache("categories:all")

    return {"message": "Category deleted"}