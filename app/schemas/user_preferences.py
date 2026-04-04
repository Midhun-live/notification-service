from pydantic import BaseModel
from typing import Optional

class UserPreferencesBase(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = True
    push_enabled: bool = True

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(UserPreferencesBase):
    pass

class UserPreferencesResponse(UserPreferencesBase):
    user_id: str

    class Config:
        from_attributes = True

class UserPreferencesRequest(UserPreferencesBase):
    pass
