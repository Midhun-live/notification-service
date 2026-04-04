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


    def create_notification(self, data: NotificationCreate) -> Notifications:
        from app.core.redis import enqueue_notification_job
        
        notification = self.repo.create(data)
        
        job_data = {
            "notification_id": str(notification.id),
            "user_id": str(notification.user_id),
            "channels": notification.channels,
            "message": notification.message
        }
        enqueue_notification_job(job_data)
        
        return notification

