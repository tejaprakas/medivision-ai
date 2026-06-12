"""
Redis Configuration
Redis connection for caching, sessions, and real-time features.
"""

import logging
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger("medivision.redis")

redis_client: redis.Redis = None


async def init_redis():
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Caching will be disabled.")
        redis_client = None


async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")


def get_redis():
    """Get Redis client instance."""
    return redis_client


async def cache_get(key: str):
    """Get value from cache."""
    if redis_client:
        try:
            return await redis_client.get(key)
        except Exception:
            pass
    return None


async def cache_set(key: str, value: str, expire: int = 3600):
    """Set value in cache with expiration."""
    if redis_client:
        try:
            await redis_client.set(key, value, ex=expire)
        except Exception:
            pass


async def cache_delete(key: str):
    """Delete value from cache."""
    if redis_client:
        try:
            await redis_client.delete(key)
        except Exception:
            pass
