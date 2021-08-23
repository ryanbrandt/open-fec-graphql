import pickle
import json
import functools
import hashlib
from typing import Callable
from flask import request

from .cache import cache, KEY_EXPIRE_TIME
from app.utils.setup_logger import get_logger


def __key_to_hash(key: tuple):
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


def cached_query(fn: Callable):
    LOGGER = get_logger(__name__)

    def sync_wrapper(*args, **kwargs):

        @functools.wraps(fn)
        async def async_wrapped():
            should_check_cache = request.headers.get(
                'Cache-control') != 'no-cache'

            if should_check_cache:
                # skip positional self, info arguments
                additional_args = args[2::] if len(args) > 2 else []

                key = (fn.__name__,) + tuple(additional_args) + \
                    tuple(*sorted(kwargs.items()))
                hash = __key_to_hash(key)

                cached_result = cache.get(hash)
                if cached_result:
                    LOGGER.info(f'Cache hit on query, returning cached result')
                    return pickle.loads(cached_result)

            result = await fn(*args, **kwargs)
            cache.set(hash, pickle.dumps(result), ex=KEY_EXPIRE_TIME)

            return result

        return async_wrapped()

    return sync_wrapper
