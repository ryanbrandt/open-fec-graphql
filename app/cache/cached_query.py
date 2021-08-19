import pickle
import json
import functools
import hashlib

from .cache import cache
from app.utils.setup_logger import get_logger


def cached_query(fn):
    LOGGER = get_logger(__name__)

    def key_to_hash(key: tuple):
        hash = hashlib.md5()

        for k in key:
            if k:
                encoded_str = bytes()
                if isinstance(k, str):
                    encoded_str = k.encode()
                else:
                    encoded_str = json.dumps(k.__dict__).encode()

                hash.update(encoded_str)

        return hash.hexdigest()

    def sync_wrapper(*args, **kwargs):

        @functools.wraps(fn)
        async def async_wrapped():
            # skip positional self, info arguments
            additional_args = args[2::] if len(args) > 2 else []

            key = (fn.__name__,) + tuple(additional_args) + \
                tuple(*sorted(kwargs.items()))
            hash = key_to_hash(key)

            cached_result = cache.get(hash)
            if cached_result:
                LOGGER.info(f'Cache hit on query, returning cached result')
                return pickle.loads(cached_result)

            result = await fn(*args, **kwargs)
            cache.set(hash, pickle.dumps(result))

            return result

        return async_wrapped()

    return sync_wrapper
