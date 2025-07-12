# app/utils/cache.py

import os
import json
import redis.asyncio as aioredis

# Redis connection URL (set this in your .env file for production)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = 600  # 10 minutes in seconds

# Create a single Redis client instance (reuse this in your app)
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_cached_chatrooms(user_id: str):
    """
    Get cached chatroom list for a user from Redis.
    Returns the Python object or None.
    """
    key = f"chatrooms:{user_id}"
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cached_chatrooms(user_id: str, chatrooms):
    """
    Cache the chatroom list for a user in Redis.
    Pass chatrooms as a serializable Python object (e.g., list of dicts).
    """
    key = f"chatrooms:{user_id}"
    if chatrooms is None:
        await redis_client.delete(key)
    else:
        await redis_client.set(key, json.dumps(chatrooms), ex=CACHE_TTL)

# Example for rate limiting (optional, for your message endpoint)
async def get_daily_message_count(user_id: str):
    key = f"daily_count:{user_id}"
    count = await redis_client.get(key)
    return int(count) if count else 0

async def increment_daily_message_count(user_id: str):
    key = f"daily_count:{user_id}"
    # Set expiry to midnight if not exists
    exists = await redis_client.exists(key)
    count = await redis_client.incr(key)
    if not exists:
        # Set expiry to next midnight
        from datetime import datetime, timedelta
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = int((tomorrow - now).total_seconds())
        await redis_client.expire(key, seconds_until_midnight)
    return count
