import json
import time
import random
from datetime import datetime, timedelta
from app.core.redis import redis_client
from app.core.database import SessionLocal
from app.models.notifications import Notifications
from app.services.channels.factory import get_handler

def _trigger_webhook(db, notification, job_data):
    try:
        from app.repositories.webhooks import WebhookRepository
        repo = WebhookRepository(db)
        webhook = repo.get_by_user_id(notification.user_id)
        if webhook:
            import requests
            payload = {
                "notification_id": str(notification.id),
                "user_id": notification.user_id,
                "status": notification.status,
                "message": notification.message,
                "channels": job_data.get("channels", [])
            }
            try:
                requests.post(webhook.url, json=payload, timeout=5)
            except Exception as e:
                print(f"Error sending webhook: {e}")
    except Exception as e:
        print(f"Error fetching webhook: {e}")

def process_job(job_data: dict):
    print(f"[*] Processing job: {json.dumps(job_data, indent=2)}")
    print(f"🔥 Processing {job_data.get('priority')} notification")
    
    # 1. Extract job data details for logging/tracking
    channels = job_data.get("channels", [])
    user_id = job_data.get("user_id")


    # 2. Update DB
    db = SessionLocal()
    try:
        notification_id = job_data.get("notification_id")
        if notification_id:
            notification = db.query(Notifications).filter(Notifications.id == notification_id).first()
            if notification:
                # Mark as sent
                notification.status = "sent"
                db.commit()
                print(f"[*] Updated status to 'sent' in DB for {notification_id}")

                # Simulate delivery using channel handlers
                for channel in notification.channels:
                    handler = get_handler(channel)
                    if not handler:
                        continue
                        
                    success = handler.send(notification.user_id, notification.message)

                if success:
                    notification.status = "delivered"
                    db.commit()
                    print(f"[*] Delivery simulation: DELIVERED for {notification_id}")
                    _trigger_webhook(db, notification, job_data)
                    return

                # 🔥 FAILURE HANDLING (FIXED)

                # ALWAYS enter retry path first
                if notification.retry_count < notification.max_retries:
                    notification.retry_count += 1

                    delay = 2 ** notification.retry_count
                    notification.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)

                    db.commit()

                    print(f"[*] Delivery failed. Requeueing {notification_id} (Attempt {notification.retry_count}/{notification.max_retries})")

                    priority = job_data.get("priority", "normal")
                    queue_name = f"notification_queue:{priority}"
                    redis_client.lpush(queue_name, json.dumps(job_data))

                    return   # 🔥 CRITICAL (prevents falling to final failure)

                # 🔥 ONLY here we mark final failure
                notification.status = "failed"
                db.commit()
                print(f"[*] Delivery simulation: FAILED permanently for {notification_id}")
                _trigger_webhook(db, notification, job_data)
            else:
                print(f"[!] Notification {notification_id} not found in DB")
    except Exception as e:
        print(f"[!] DB Error: {e}")
    finally:
        db.close()

def run_worker():
    print("[*] Worker started. Waiting for jobs... (Priorities: critical, high, normal, low)")
    while True:
        try:
            # BRPOP blocks until a job is available in the queue
            # Returns a tuple: (queue_name, data)
            result = redis_client.brpop(
                ["notification_queue:critical", "notification_queue:high", "notification_queue:normal", "notification_queue:low"],
                timeout=0
            )
            if result:
                _, job_json = result
                job_data = json.loads(job_json)
                process_job(job_data)
        except Exception as e:
            print(f"[!] Worker Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_worker()
