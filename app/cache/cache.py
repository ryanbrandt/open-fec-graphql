from redis import Redis


cache = Redis(host='redis-cache', port=6379, db=0)
