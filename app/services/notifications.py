from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.notifications import NotificationRepository
from app.schemas.notifications import NotificationCreate
from app.models.notifications import Notifications
import uuid
from typing import List

class NotificationService:
    def __init__(self, db: Session):
        self.repo = NotificationRepository(db)

    def get_notification(self, notification_id: uuid.UUID) -> Notifications:
        notification = self.repo.get_by_id(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification

    def get_user_notifications(self, user_id: str) -> List[Notifications]:
        return self.repo.get_by_user_id(user_id)


    def create_notification(self, data: NotificationCreate) -> tuple[Notifications, bool]:
        from app.services.template_service import TemplateService
        
        if data.template:
            data.message = TemplateService.render(data.template, data.variables)
        elif not data.message:
            raise HTTPException(status_code=400, detail="Either message or template must be provided")
            
        if data.idempotency_key:
            existing_notification = self.repo.get_by_idempotency_key(data.idempotency_key)
            if existing_notification:
                return existing_notification, False

        notification = self.repo.create(data)
        return notification, True
    def create_batch_notifications(self, data: "app.schemas.notifications.NotificationBatchCreate"):
        from app.core.redis import enqueue_notification_job, redis_client
        from app.schemas.notifications import NotificationCreate, NotificationBatchResponse, BatchNotificationDetail
        
        details = []
        success = 0
        failed = 0
        
        for user_id in data.user_ids:
            rate_limit_key = f"rate_limit:{user_id}"
            current_count = redis_client.incr(rate_limit_key)
            if current_count == 1:
                redis_client.expire(rate_limit_key, 3600)
                
            if current_count > 100:
                details.append(BatchNotificationDetail(
                    user_id=user_id,
                    status="rate_limited"
                ))
                failed += 1
                continue
                
            # Scope idempotency_key to user for batch requests
            user_idempotency_key = f"{data.idempotency_key}_{user_id}" if data.idempotency_key else None
            
            create_data = NotificationCreate(
                user_id=user_id,
                message=data.message,
                channels=data.channels,
                priority=data.priority,
                idempotency_key=user_idempotency_key,
                batch_id=data.batch_id,
                metadata=data.metadata,
                template=data.template,
                variables=data.variables
            )
            
            notification, is_new = self.create_notification(create_data)
            
            if is_new:
                job_data = {
                    "notification_id": str(notification.id),
                    "user_id": str(notification.user_id),
                    "channels": notification.channels,
                    "message": notification.message,
                    "priority": notification.priority
                }
                enqueue_notification_job(job_data)
                
            details.append(BatchNotificationDetail(
                user_id=user_id,
                status="created" if is_new else "duplicate",
                notification_id=notification.id
            ))
            success += 1
            
        return NotificationBatchResponse(
            total=len(data.user_ids),
            success=success,
            failed=failed,
            details=details
        )
