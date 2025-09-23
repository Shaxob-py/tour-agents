import asyncio
import sys
import json
import random
from pathlib import Path
from datetime import timedelta, date

from faker import Faker
from passlib.context import CryptContext
from sqlalchemy import select

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from database.base_model import db
from database import Country, User, Trip
from database.countries import City

fake = Faker()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
FIXTURE_PATH = BASE_DIR / "utils" / "fixtures" / "countries.json"


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)


async def seed_countries():
    if not FIXTURE_PATH.exists():
        print("⚠️ No countries.json file")
        return
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data:
        exists = await db.execute(select(Country).where(Country.name == c["name"]))
        if not exists.scalars().first():
            db.add(Country(name=c["name"], code=c["code"]))

    await db.commit()
    print(f"✅ Countries seeded (unique only)")


async def seed_cities():
    result = await db.execute(select(Country))
    countries = result.scalars().all()

    for country in countries:
        for _ in range(2):
            city_name = fake.unique.city()  # unique nom olamiz
            exists = await db.execute(select(City).where(City.name == city_name))
            if not exists.scalars().first():
                db.add(City(name=city_name, country_id=country.id))

    await db.commit()
    print("✅ Cities added (unique only)")


async def seed_users(n=10):
    for i in range(n):
        db.add(User(
            username=f"user{i}",
            phone_number="998" + fake.msisdn()[:9],
            telegram_id=random.randint(100000, 999999),
            password=hash_password("password123"),
        ))
    await db.commit()
    print(f"✅ {n} users added")


async def seed_trips(n=20):
    users = (await db.execute(select(User))).scalars().all()
    countries = (await db.execute(select(Country))).scalars().all()
    for _ in range(n):
        start = date.today() - timedelta(days=random.randint(1, 60))
        end = start + timedelta(days=random.randint(1, 10))
        db.add(Trip(
            away_from=fake.city(),
            destination=random.choice(countries).name,
            days=(end - start).days + 1,
            description=fake.paragraph(),
            start_date=start,
            end_date=end,
            user_id=random.choice(users).id
        ))
    await db.commit()
    print(f"✅ {n} trips added")


async def main():
    await seed_countries()
    await seed_cities()
    await seed_users()
    await seed_trips()
    print("🎉 Fake data seeding completed")


if __name__ == "__main__":
    asyncio.run(main())
