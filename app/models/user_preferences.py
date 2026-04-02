import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(String, unique=True, nullable=False)

    email_enabled = Column(Boolean, default=True)

    sms_enabled = Column(Boolean, default=True)

    push_enabled = Column(Boolean, default=True)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())