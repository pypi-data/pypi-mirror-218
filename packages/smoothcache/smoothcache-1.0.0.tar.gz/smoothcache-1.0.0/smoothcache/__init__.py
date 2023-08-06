#!/usr/bin/env python3

from functools import wraps

from .smooth import CacheController
from .exceptions import (
    KeyAlreadyExistsError,
    EntryNotFoundError,
    EntryExpiredError,
)

Cache = CacheController()


def cache_function(ttl=None):
    """Cache the output of the decorated function.

    This function decorator is experimental and may not
    work as expected.

    .. attention:
        All parameters passed to a cached function MUST implement
        a `__hash__` function.
    """

    def _hash_parameters(args, kwargs):
        param_hash = ""
        for arg in args:
            param_hash += str(hash(arg))

        for _, v in kwargs.items():
            param_hash += str(hash(v))

        return param_hash

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            param_hash = _hash_parameters(args, kwargs)

            cache_key = f"{func.__name__}_{param_hash}"

            try:
                cache_result = Cache.get(cache_key, default=None)
                if cache_result is None:
                    raise Exception

                return cache_result.value

            except Exception:
                # Cache Miss, call the original function and save
                #  the value in cache.
                return_value = func(*args, **kwargs)
                Cache.set(cache_key, return_value, ttl=ttl)
                return return_value

        return wrapper
    return decorate


__all__ = [
    "Cache",
    "CacheController",
    "KeyAlreadyExistsError",
    "EntryNotFoundError",
    "EntryExpiredError",
    "cache_function",
]
