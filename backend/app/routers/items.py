from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)) -> list[ItemResponse]:
    """List all items. TODO: pagination, filtering, eager-load category."""
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return [ItemResponse.model_validate(item) for item in items]


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    """Create an item. TODO: validate category_id; enforce unique SKU."""
    item = Item(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ItemResponse.model_validate(item)
