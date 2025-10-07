from sqlalchemy.future import select
from database.base_model import db
from database.support import SupportMessage
from schemas.base_schema import CreateSupportSchema
from database import User


async def create_support_message(data: CreateSupportSchema, current_user: User):
        new_msg = SupportMessage(
            message=data.message,
            user_id=current_user.id,
            phone_number=current_user.phone_number,
        )
        db.add(new_msg)
        await db.commit()
        await db.refresh(new_msg)
        return new_msg


async def get_support_messages():
        result = await db.execute(select(SupportMessage))
        return result.scalars().all()
