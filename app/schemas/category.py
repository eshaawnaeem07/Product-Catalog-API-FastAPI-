from pydantic import BaseModel
from typing import Optional


# Used when creating a category (POST)
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


# Used when updating a category (PUT / PATCH)
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Used when returning category response
class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # for SQLAlchemy (Pydantic v2)