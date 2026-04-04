from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_preferences import UserPreferencesRepository
from app.schemas.user_preferences import UserPreferencesRequest, UserPreferencesResponse
from app.models.user_preferences import UserPreferences

class UserPreferencesService:
    def __init__(self, db: Session):
        self.repo = UserPreferencesRepository(db)

    def get_user_preferences(self, user_id: str) -> UserPreferences:
        prefs = self.repo.get_by_user_id(user_id)
        if not prefs:
            raise HTTPException(status_code=404, detail="User preferences not found")
        return prefs

    def upsert_user_preferences(self, user_id: str, request_data: UserPreferencesRequest) -> UserPreferences:
        # Business logic goes here (if any apart from repository ops)
        return self.repo.upsert(user_id, request_data)
