# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.schemas.product import *
# from app.crud import product as crud
# from app.api.deps import get_current_user
# from app.cache import *
# from app.cache import get_cache, set_cache, delete_cache

# router = APIRouter(prefix="/products", tags=["Products"])

# @router.get("/", response_model=list[ProductOut])
# def list_products(
#     category_id: int | None = None,
#     db: Session = Depends(get_db)
# ):
#     cache_key = f"products:{category_id or 'all'}"
#     cached = get_cache(cache_key)

#     if cached:
#         return cached

#     products = crud.get_products(db, category_id)

#     result = [ProductOut.model_validate(p).model_dump() for p in products]

#     set_cache(cache_key, result)

#     return result

# @router.get("/{id}", response_model=ProductOut)
# def get_product(id: int, db: Session = Depends(get_db)):
#     cache_key = f"product:{id}"
#     cached = get_cache(cache_key)
#     if cached:
#         return cached

#     product = crud.get_product(db, id)
#     if not product:
#         raise HTTPException(404)
#     set_cache(cache_key, ProductOut.model_validate(product).model_dump())
#     return product

# @router.post("/", response_model=ProductOut, status_code=201)
# def create(product: ProductCreate,
#            db: Session = Depends(get_db),
#            user=Depends(get_current_user)):
#     return crud.create_product(db, product)

# @router.put("/{id}", response_model=ProductOut)
# def update(id: int,
#            data: ProductUpdate,
#            db: Session = Depends(get_db),
#            user=Depends(get_current_user)):
#     db_obj = crud.get_product(db, id)
#     if not db_obj:
#         raise HTTPException(404)
#     delete_cache(f"product:{id}")
#     return crud.update_product(db, db_obj, data)

# @router.delete("/{id}", status_code=200)
# def delete(id: int,
#            db: Session = Depends(get_db),
#            user=Depends(get_current_user)):
#     db_obj = crud.get_product(db, id)
#     if not db_obj:
#         raise HTTPException(404)
#     crud.delete_product(db, db_obj)
#     delete_cache(f"product:{id}")
#     return {"detail": "Deleted"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud import product as crud
from app.api.deps import get_current_user
from app.cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/products", tags=["Products"])


# LIST PRODUCTS
@router.get("/", response_model=list[ProductOut])
def list_products(
    category_id: int | None = None,
    db: Session = Depends(get_db)
):

    cache_key = f"products:{category_id or 'all'}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    products = crud.get_products(db, category_id)

    result = [ProductOut.model_validate(p).model_dump() for p in products]

    set_cache(cache_key, result)

    return result


# GET SINGLE PRODUCT
@router.get("/{id}", response_model=ProductOut)
def get_product(id: int, db: Session = Depends(get_db)):

    cache_key = f"product:{id}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    product = crud.get_product(db, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    result = ProductOut.model_validate(product).model_dump()

    set_cache(cache_key, result)

    return result


# CREATE PRODUCT
@router.post("/", response_model=ProductOut, status_code=201)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    new_product = crud.create_product(db, product)

    # invalidate product list cache
    delete_cache("products:all")

    return new_product


# UPDATE PRODUCT
@router.put("/{id}", response_model=ProductOut)
def update(
    id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    db_obj = crud.get_product(db, id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Product not found")

    updated = crud.update_product(db, db_obj, data)

    delete_cache(f"product:{id}")
    delete_cache("products:all")

    return updated


# DELETE PRODUCT
@router.delete("/{id}", status_code=200)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    db_obj = crud.get_product(db, id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.delete_product(db, db_obj)

    delete_cache(f"product:{id}")
    delete_cache("products:all")

    return {"detail": "Deleted"}