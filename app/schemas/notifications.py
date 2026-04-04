from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

class NotificationCreate(BaseModel):
    user_id: str
    message: str
    channels: List[str]
    priority: str
    idempotency_key: Optional[str] = None
    batch_id: Optional[uuid.UUID] = None
    metadata: Optional[Dict[str, Any]] = None

class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    message: str
    channels: List[str]
    priority: str
    status: str

    class Config:
        from_attributes = True
