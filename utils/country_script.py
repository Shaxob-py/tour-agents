import asyncio
import json
import os
import sys
from pathlib import Path
from sqlalchemy import select
from database.base_model import db

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(os.path.join(BASE_DIR, '..'))

from core.config import settings
from database import Country

DATABASE_URL = settings.postgres_async_url
FIXTURE_PATH = BASE_DIR / 'fixtures' / "countries.json"


async def add_countries():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    stmt = select(Country.name).where(Country.name.in_([c["name"] for c in data]))
    result = await db.execute(stmt)
    existing = {row[0] for row in result.fetchall()}

    new_countries = [c for c in data if c["name"] not in existing]
    if new_countries:
        for c in new_countries:
            db.add(Country(code=c["code"], name=c["name"]))
        await db.commit()

    return len(new_countries), len(existing)


def main():
    try:
        new_count, existing_count = asyncio.run(add_countries())
        print(f"✅ {new_count} new countries added.")
        print(f"ℹ️  {existing_count} countries already existed in database.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()
