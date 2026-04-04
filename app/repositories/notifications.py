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


    def create(self, data: NotificationCreate) -> Notifications:
        data_dict = data.model_dump(exclude_unset=True)
        # Handle the field name mapping from API 'metadata' to DB 'meta_data'
        if "metadata" in data_dict:
            data_dict["meta_data"] = data_dict.pop("metadata")
            
        db_obj = Notifications(**data_dict)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
