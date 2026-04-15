from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from utils.pydantic_utils import PyObjectId


class NotificationQueueCreate(BaseModel):
    fcm_token: str
    message: str
    medicine_id: str


class NotificationQueueItem(NotificationQueueCreate):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
