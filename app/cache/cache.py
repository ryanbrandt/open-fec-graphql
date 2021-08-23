from redis import Redis

KEY_EXPIRE_TIME = 10000

cache = Redis(host='redis-cache', port=6379, db=0)
