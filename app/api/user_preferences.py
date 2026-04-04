from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_preferences import UserPreferencesRequest, UserPreferencesResponse
from app.services.user_preferences import UserPreferencesService

router = APIRouter()

@router.get("/users/{user_id}/preferences", response_model=UserPreferencesResponse)
def get_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    service = UserPreferencesService(db)
    return service.get_user_preferences(user_id)

@router.post("/users/{user_id}/preferences", response_model=UserPreferencesResponse)
def upsert_preferences(
    user_id: str,
    request: UserPreferencesRequest,
    db: Session = Depends(get_db)
):
    service = UserPreferencesService(db)
    return service.upsert_user_preferences(user_id, request)
