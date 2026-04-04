from sqlalchemy.orm import Session
from typing import Optional
from app.models.user_preferences import UserPreferences
from app.schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate

class UserPreferencesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: str) -> Optional[UserPreferences]:
        return self.db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()

    def create(self, user_id: str, data: UserPreferencesCreate) -> UserPreferences:
        db_obj = UserPreferences(user_id=user_id, **data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: UserPreferences, data: UserPreferencesUpdate) -> UserPreferences:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def upsert(self, user_id: str, data: UserPreferencesCreate) -> UserPreferences:
        existing = self.get_by_user_id(user_id)
        if existing:
            return self.update(existing, UserPreferencesUpdate(**data.model_dump()))
        return self.create(user_id, data)
