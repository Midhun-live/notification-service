import random
import time

class PushHandler:
    def send(self, user_id: str, message: str) -> bool:
        """
        Simulate sending notification.
        Return True (success) or False (failure)
        """
        print(f"[*] Simulating Push sending to user {user_id}...")
        time.sleep(1)
        return random.choice([True, False])
