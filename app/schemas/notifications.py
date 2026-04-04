from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

class NotificationCreate(BaseModel):
    user_id: str
    message: Optional[str] = None
    template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    channels: List[str]
    priority: str = "normal"
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

class NotificationBatchCreate(BaseModel):
    user_ids: List[str]
    message: Optional[str] = None
    template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    channels: List[str]
    priority: str = "normal"
    idempotency_key: Optional[str] = None
    batch_id: Optional[uuid.UUID] = None
    metadata: Optional[Dict[str, Any]] = None

class BatchNotificationDetail(BaseModel):
    user_id: str
    status: str
    notification_id: Optional[uuid.UUID] = None

class NotificationBatchResponse(BaseModel):
    total: int
    success: int
    failed: int
    details: List[BatchNotificationDetail]
