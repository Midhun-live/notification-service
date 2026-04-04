import random
import time

class SMSHandler:
    def send(self, user_id: str, message: str) -> bool:
        print(f"Simulating SMS sending to user {user_id}")
        time.sleep(1)
        return random.choice([True, False])
