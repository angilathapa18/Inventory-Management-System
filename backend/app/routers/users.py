from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    """List users with role. TODO: admin-only; pagination."""
    result = await db.execute(
        select(User).options(selectinload(User.role))
    )
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create a user. TODO: hash password; validate role_id."""
    data = payload.model_dump(exclude={"password"})
    user = User(**data, password_hash=payload.password)
    db.add(user)
    await db.commit()

    result = await db.execute(
        select(User)
        .where(User.user_id == user.user_id)
        .options(selectinload(User.role))
    )
    user = result.scalar_one()
    return UserResponse.model_validate(user)
