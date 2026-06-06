"""Verify Supabase connection. Run from backend/: python scripts/test_db.py"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from app.config import settings
from app.database import engine


async def main() -> None:
    host = settings.database_url.split("@")[-1].split("/")[0]
    print(f"Connecting to: {host}")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT current_database(), version()"))
            row = result.one()
            print(f"Connected to database: {row[0]}")
            print(f"PostgreSQL: {row[1][:60]}...")
    except OSError as exc:
        print(
            "\nDNS failed (getaddrinfo). Use Supabase Session pooler URI, not db.*.supabase.co"
        )
        raise SystemExit(1) from exc


if __name__ == "__main__":
    asyncio.run(main())
