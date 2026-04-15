import asyncio
from datetime import datetime, timedelta
from database import get_db
from utils.firebase import send_push_notification


async def notification_cron_job():
    """Background cron job that processes the notification queue.

    Runs in a loop every 60 seconds:
    - Picks up queue items that are 5+ minutes old
    - Checks if the medicine log state is still not "taken"
    - If not taken: sends the Firebase push notification
    - Removes processed items from the queue either way
    - If the queue is empty: sleeps (does nothing)
    """
    print("Notification cron job started.")
    while True:
        try:
            db = get_db()
            if db is None:
                await asyncio.sleep(60)
                continue

            cutoff = datetime.utcnow() - timedelta(minutes=5)

            # Find items that have been waiting 5+ minutes
            items = await db.notification_queue.find(
                {"created_at": {"$lte": cutoff}}
            ).to_list(length=None)

            if not items:
                # Queue is empty or nothing mature yet — sleep
                await asyncio.sleep(60)
                continue

            for item in items:
                medicine_id = item.get("medicine_id")
                fcm_token = item.get("fcm_token")
                message = item.get("message", "")

                # Check current medicine log state for this medicine
                log = await db.medicine_logs.find_one(
                    {"medicine_id": medicine_id},
                    sort=[("date", -1), ("time", -1)],
                )

                state = log.get("state", "pending") if log else "pending"

                if state != "taken":
                    # Medicine not taken — send notification
                    send_push_notification(
                        fcm_token=fcm_token,
                        title="Medicine Reminder",
                        body=message,
                    )
                    print(f"Notification sent for medicine {medicine_id}")
                else:
                    print(f"Medicine {medicine_id} already taken. Skipping notification.")

                # Remove from queue either way
                await db.notification_queue.delete_one({"_id": item["_id"]})

        except asyncio.CancelledError:
            print("Notification cron job cancelled.")
            break
        except Exception as e:
            print(f"Notification cron job error: {e}")

        await asyncio.sleep(60)
