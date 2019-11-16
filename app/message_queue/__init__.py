import os

import redis
from huey import RedisHuey
from huey.consumer import Consumer

huey = RedisHuey(
    name='tochka_huey',
    immediate=os.getenv('HUEY_IMMEDIATE', '0') == '1',
    connection_pool=redis.ConnectionPool(
        max_connections=50,
        host=os.environ.get('REDIS_HOST', '127.0.0.1'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
    ),
)

consumer = Consumer(
    huey=huey,
    workers=int(os.getenv('HUEY_WORKERS', 1)),
    worker_type=os.getenv('HUEY_WORKER_TYPE', 'thread'),
    check_worker_health=True,
    health_check_interval=1,
)
