from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------


class ItemBase(BaseModel):
    name: str = Field(..., max_length=200)
    sku: str = Field(..., max_length=50)
    category_id: int | None = None
    reorder_level: int = 10
    unit_price: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    item_id: int


# ---------------------------------------------------------------------------
# User & Role
# ---------------------------------------------------------------------------


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_id: int
    role_name: str = Field(..., max_length=50)
    description: str | None = None


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=100)
    role_id: int | None = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plain text; hash before persist")


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    created_at: datetime
    last_login: datetime | None = None
    role: RoleResponse | None = None
