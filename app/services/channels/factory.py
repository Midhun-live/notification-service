from app.services.channels.email_handler import EmailHandler
from app.services.channels.sms_handler import SMSHandler
from app.services.channels.push_handler import PushHandler

def get_handler(channel: str):
    if channel == "email":
        return EmailHandler()
    elif channel == "sms":
        return SMSHandler()
    elif channel == "push":
        return PushHandler()
    else:
        return None
