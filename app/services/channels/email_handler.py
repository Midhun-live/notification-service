import random
import time

class EmailHandler:
    def send(self, user_id: str, message: str) -> bool:
        print(f"Simulating Email sending to user {user_id}")
        time.sleep(1)
        return random.choice([True, False])
