"""Insert starter roles, locations, and categories. Run after init_db."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Category, Location, Role

ROLES = [
    ("ADMIN", "Full system access and user management"),
    ("MANAGER", "Can edit inventory and view reports"),
    ("STAFF", "Can perform check-ins and check-outs"),
]

LOCATIONS = [
    ("Main Warehouse", "123 Supply Chain Road"),
    ("Tech Lab", "456 Innovation Drive"),
]

CATEGORIES = [
    ("Laptops", "Company issued computers"),
    ("Peripherals", "Mice, Keyboards, Monitors"),
    ("Stationery", "Bulk office supplies"),
]


async def main() -> None:
    async with AsyncSessionLocal() as session:
        for role_name, description in ROLES:
            exists = await session.scalar(
                select(Role.role_id).where(Role.role_name == role_name)
            )
            if not exists:
                session.add(Role(role_name=role_name, description=description))

        for name, address in LOCATIONS:
            exists = await session.scalar(
                select(Location.location_id).where(Location.name == name)
            )
            if not exists:
                session.add(Location(name=name, address=address))

        for name, description in CATEGORIES:
            exists = await session.scalar(
                select(Category.category_id).where(Category.name == name)
            )
            if not exists:
                session.add(Category(name=name, description=description))

        await session.commit()
    print("Seed data applied.")


if __name__ == "__main__":
    asyncio.run(main())
