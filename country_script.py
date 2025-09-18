import asyncio
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
from database import Country

DATABASE_URL = settings.postgres_async_url

COUNTRIES: List[str] = [
    "Uzbekistan", "Kazakhstan", "Kyrgyzstan", "Turkey", "Russia", "China",
    "Japan", "France", "Spain", "United States", "Italy", "Mexico",
    "United Kingdom", "Germany", "Greece", "Thailand", "Austria", "United Arab Emirates",
    "Saudi Arabia", "Portugal", "Malaysia", "Hong Kong", "Netherlands", "India",
]


async def add_countries(names: List[str]):
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # noqa

    try:
        async with AsyncSessionLocal() as session:
            stmt = select(Country.name).where(Country.name.in_(names))
            result = await session.execute(stmt)
            existing = {row[0] for row in result.fetchall()}

            new_countries = [name for name in names if name not in existing]
            if new_countries:
                for name in new_countries:
                    session.add(Country(name=name))
                await session.commit()
            return len(new_countries), len(existing)

    finally:
        await engine.dispose()


def main():
    try:
        new_count, existing_count = asyncio.run(add_countries(COUNTRIES))
        print(f"✅ {new_count} new countries added.")
        print(f"ℹ️  {existing_count} countries already existed in database.")
    except Exception as e:
        print(f"❌ Error: {e}")
