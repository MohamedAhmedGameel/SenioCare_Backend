from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import get_db
from schemas.notification_queue import NotificationQueueCreate

router = APIRouter()


@router.post("/queue", status_code=201)
async def queue_notification(payload: NotificationQueueCreate):
    """Queue a notification to be sent after 5 minutes if medicine is not taken.

    The Flutter app sends:
    - fcm_token: the caregiver's Firebase device token
    - message: the notification body text
    - medicine_id: the daily_medicine ID to check
    """
    db = get_db()

    doc = payload.model_dump()
    doc["created_at"] = datetime.utcnow()

    await db.notification_queue.insert_one(doc)

    return {"message": "Notification queued"}
