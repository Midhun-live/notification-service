from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.notifications import NotificationRepository
from app.schemas.notifications import NotificationCreate
from app.models.notifications import Notifications
import uuid

class NotificationService:
    def __init__(self, db: Session):
        self.repo = NotificationRepository(db)

    def get_notification(self, notification_id: uuid.UUID) -> Notifications:
        notification = self.repo.get_by_id(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification


    def create_notification(self, data: NotificationCreate) -> tuple[Notifications, bool]:
        if data.idempotency_key:
            existing_notification = self.repo.get_by_idempotency_key(data.idempotency_key)
            if existing_notification:
                return existing_notification, False

        notification = self.repo.create(data)
        return notification, True

