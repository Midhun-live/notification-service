import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import NotificationStatus, NotificationPriority


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(String, index=True, nullable=False)

    message = Column(Text, nullable=False)

    channels = Column(JSON, nullable=False)

    priority = Column(String, nullable=False, default=NotificationPriority.NORMAL.value)

    status = Column(String, nullable=False, default=NotificationStatus.PENDING.value)

    idempotency_key = Column(String, unique=True, nullable=True)

    batch_id = Column(UUID(as_uuid=True), nullable=True, index=True)

    meta_data = Column(JSON, nullable=True)

    retry_count = Column(Integer, default=0)

    max_retries = Column(Integer, default=3)

    next_retry_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())