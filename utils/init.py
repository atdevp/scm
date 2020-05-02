import redis
import cfg
import logging

logger = logging.getLogger('scm')


def load_redis_connect_pool():
    pool = redis.ConnectionPool(
        host=cfg.REDIS['host'],
        port=cfg.REDIS['port'],
        db=cfg.REDIS['db'],
        max_connections=cfg.REDIS['max_connections']
    )

    conn = None
    try:
        conn = redis.Redis(connection_pool=pool, socket_connect_timeout=cfg.REDIS['connect_timeout'])
        logger.info("connected redis successful")
    except Exception as e:  
        logger.error(str(e))

    return conn


RedisPool = load_redis_connect_pool()
