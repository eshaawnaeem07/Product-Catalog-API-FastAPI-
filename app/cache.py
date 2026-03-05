import redis
import json
from fastapi.encoders import jsonable_encoder

# connect to redis server
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cache(key: str, value, expire: int = 60):
    # Convert datetime and other non-serializable objects
    encoded_value = jsonable_encoder(value)

    redis_client.setex(
        key,
        expire,
        json.dumps(encoded_value)
    )


def delete_cache(key: str):
    redis_client.delete(key)