import time

from aredis_om import Field, HashModel

from app.db.redis.session import redis_conn


class Item(HashModel):
    name: str = Field(index=True)
    timestamp: float = Field(default=time.time(), index=True)

    class Meta:
        database = redis_conn
