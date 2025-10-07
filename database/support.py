from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from sqlalchemy.orm import relationship

from database.base_model import Base


class SupportMessage(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user = relationship("User", back_populates="support_messages")
    message = Column(Text, nullable=False)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=None))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
