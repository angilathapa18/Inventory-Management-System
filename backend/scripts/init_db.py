"""Create all tables from SQLAlchemy models (dev/bootstrap). Run from backend/."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, engine
from app import models  # noqa: F401


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created (or already exist).")


if __name__ == "__main__":
    asyncio.run(main())
