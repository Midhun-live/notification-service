from sqlalchemy.orm import Session
from app.models.webhooks import Webhooks
from app.schemas.webhooks import WebhookCreate
from typing import Optional

class WebhookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: str) -> Optional[Webhooks]:
        return self.db.query(Webhooks).filter(Webhooks.user_id == user_id).first()

    def create(self, data: WebhookCreate) -> Webhooks:
        # Avoid duplicate webhooks for the same user, or just update
        existing = self.get_by_user_id(data.user_id)
        if existing:
            existing.url = str(data.url)
            self.db.commit()
            self.db.refresh(existing)
            return existing

        db_obj = Webhooks(user_id=data.user_id, url=str(data.url))
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
