from sqlalchemy.orm import Session
from app.models.notifications import Notifications
from app.schemas.notifications import NotificationCreate
from typing import Optional
import uuid

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, notification_id: uuid.UUID) -> Optional[Notifications]:
        return self.db.query(Notifications).filter(Notifications.id == notification_id).first()

    def get_by_idempotency_key(self, idempotency_key: str) -> Optional[Notifications]:
        return self.db.query(Notifications).filter(Notifications.idempotency_key == idempotency_key).first()


    def create(self, data: NotificationCreate) -> Notifications:
        data_dict = data.model_dump(exclude_unset=True)
        if "metadata" in data_dict:
            data_dict["meta_data"] = data_dict.pop("metadata")
            
        data_dict.pop("template", None)
        data_dict.pop("variables", None)
            
        db_obj = Notifications(**data_dict)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
