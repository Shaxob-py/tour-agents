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

    result = await User.get_by_phone_number(phone_number)
    existing = result.scalar_one_or_none()
    if existing:
        print("❌ User already exists")
        return

    await User.create(
        phone_number=phone_number,
        username="superuser",
        telegram_id=54345432,
        password=User.get_password_hash(password),
        role=User.Role.ADMIN.name
    )
    print("✅ Superuser created!")
