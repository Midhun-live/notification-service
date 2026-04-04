from sqlalchemy.orm import Session
from app.repositories.user_preferences import UserPreferencesRepository
from app.schemas.user_preferences import UserPreferencesRequest, UserPreferencesResponse
from app.models.user_preferences import UserPreferences

class UserPreferencesService:
    def __init__(self, db: Session):
        self.repo = UserPreferencesRepository(db)

    def upsert_user_preferences(self, user_id: str, request_data: UserPreferencesRequest) -> UserPreferences:
        # Business logic goes here (if any apart from repository ops)
        return self.repo.upsert(user_id, request_data)
