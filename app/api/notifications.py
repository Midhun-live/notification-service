from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.core.database import get_db
from app.schemas.notifications import NotificationCreate, NotificationResponse
from app.services.notifications import NotificationService

router = APIRouter()

@router.post("/notifications", response_model=NotificationResponse)
def create_notification(
    request: NotificationCreate,
    db: Session = Depends(get_db)
):
    from app.core.redis import enqueue_notification_job
    service = NotificationService(db)
    notification, is_new = service.create_notification(request)
    
    if is_new:
        job_data = {
            "notification_id": str(notification.id),
            "user_id": str(notification.user_id),
            "channels": notification.channels,
            "message": notification.message,
            "priority": notification.priority
        }
        enqueue_notification_job(job_data)
        
    return notification

@router.get("/notifications/{id}", response_model=NotificationResponse)
def get_notification(
    id: str,
    db: Session = Depends(get_db)
):
    try:
        notification_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    service = NotificationService(db)
    return service.get_notification(notification_id)
