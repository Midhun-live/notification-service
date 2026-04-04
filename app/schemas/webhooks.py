from pydantic import BaseModel, HttpUrl
from typing import Optional
import uuid
import datetime

class WebhookCreate(BaseModel):
    user_id: str
    url: HttpUrl

class WebhookResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    url: HttpUrl
    created_at: datetime.datetime

    class Config:
        from_attributes = True
