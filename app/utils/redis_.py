from redis.asyncio import ConnectionError, Redis

from app.configs import settings

redis: "Redis[str]" = Redis.from_url(
    settings.REDIS_URL, decode_responses=True, socket_timeout=5, retry_on_timeout=True, retry_on_error=[ConnectionError]
)
