from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db as _get_db

# Re-export for route dependency injection.
get_db = _get_db

__all__ = ["get_db", "AsyncSession", "AsyncGenerator"]
