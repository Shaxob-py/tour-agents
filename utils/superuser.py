import asyncio
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(os.path.join(BASE_DIR, '..'))
from getpass import getpass

from database.users import User


async def create_superuser():
    phone_number = input("Phone number: ")
    password = getpass("Password: ")

    user = await User.get_by_phone_number(phone_number)
    if user:
        print("❌ User already exists")
        return

    await User.create(
        phone_number=phone_number,
        username="superuser",
        telegram_id=543451,
        password=User.get_password_hash(password),
        role=User.Role.ADMIN.name
    )
    print("✅ Superuser created!")


if __name__ == '__main__':
    asyncio.run(create_superuser())
