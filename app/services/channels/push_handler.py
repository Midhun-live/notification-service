import random
import time

class PushHandler:
    def send(self, user_id: str, message: str) -> bool:
        print(f"Simulating Push sending to user {user_id}")
        time.sleep(1)
        return random.choice([True, False])
