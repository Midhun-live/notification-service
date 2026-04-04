from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.webhooks import WebhookCreate, WebhookResponse
from app.services.webhooks import WebhookService

router = APIRouter()

@router.post("/webhooks", response_model=WebhookResponse)
def register_webhook(
    request: WebhookCreate,
    db: Session = Depends(get_db)
):
    service = WebhookService(db)
    return service.register_webhook(request)

@router.get("/webhooks/{user_id}", response_model=WebhookResponse)
def get_webhook(
    user_id: str,
    db: Session = Depends(get_db)
):
    service = WebhookService(db)
    return service.get_webhook(user_id)
