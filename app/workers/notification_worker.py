import json
import time
import random
from app.core.redis import redis_client
from app.core.database import SessionLocal
from app.models.notifications import Notifications

def process_job(job_data: dict):
    print(f"[*] Processing job: {json.dumps(job_data, indent=2)}")
    
    # 1. Simulate sending
    channels = job_data.get("channels", [])
    user_id = job_data.get("user_id")
    print(f"[*] Simulating sending to {channels} for user {user_id}...")
    time.sleep(1)
    print("[*] Sent successfully!")

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
                
                # Simulate delivery success/failure
                time.sleep(1) # simulate brief delivery time
                success = random.choice([True, False])
                notification.status = "delivered" if success else "failed"
                db.commit()
                print(f"[*] Delivery simulation: {notification.status.upper()} for {notification_id}")
            else:
                print(f"[!] Notification {notification_id} not found in DB")
    except Exception as e:
        print(f"[!] DB Error: {e}")
    finally:
        db.close()

def run_worker():
    print("[*] Worker started. Waiting for jobs in 'notification_queue'...")
    while True:
        try:
            # BRPOP blocks until a job is available in the queue
            # Returns a tuple: (queue_name, data)
            result = redis_client.brpop("notification_queue", timeout=0)
            if result:
                _, job_json = result
                job_data = json.loads(job_json)
                process_job(job_data)
        except Exception as e:
            print(f"[!] Worker Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_worker()
