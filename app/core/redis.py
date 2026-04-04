import redis
import json
import uuid

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def enqueue_notification_job(data: dict):
    # Convert any UUIDs to string to make JSON serializable
    dict_data = {}
    for k, v in data.items():
        if isinstance(v, uuid.UUID):
            dict_data[k] = str(v)
        else:
            dict_data[k] = v
            
    json_data = json.dumps(dict_data)
    redis_client.lpush("notification_queue", json_data)
