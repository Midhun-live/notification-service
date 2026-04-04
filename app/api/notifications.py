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
    service = NotificationService(db)
    return service.create_notification(request)

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
