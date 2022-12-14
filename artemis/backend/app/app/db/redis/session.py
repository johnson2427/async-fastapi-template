from aredis_om import get_redis_connection

from app.core.config import settings

redis_conn = get_redis_connection(
    url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True
)
