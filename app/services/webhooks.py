import httpx
import threading
from app.repositories.webhooks import WebhookRepository
from app.schemas.webhooks import WebhookCreate
from app.models.webhooks import Webhooks
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json

class WebhookService:
    def __init__(self, db: Session):
        self.repo = WebhookRepository(db)

    def register_webhook(self, data: WebhookCreate) -> Webhooks:
        return self.repo.create(data)

    def get_webhook(self, user_id: str) -> Webhooks:
        webhook = self.repo.get_by_user_id(user_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        return webhook

    @staticmethod
    def send_webhook(url: str, payload: dict):
        def _send():
            try:
                with httpx.Client(timeout=5.0) as client:
                    response = client.post(url, json=payload)
                    response.raise_for_status()
            except Exception as e:
                print(f"Webhook delivery failed for {url}: {e}")
        
        thread = threading.Thread(target=_send, daemon=True)
        thread.start()
