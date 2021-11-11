import redis

import config

r = redis.Redis(**{'host': config.REDIS_URL, 'port': 6379,
                   'decode_responses': True, 'charset': 'utf-8'})

for key in r.keys():
    if key.startswith("bordas"):
        r.delete(key)
