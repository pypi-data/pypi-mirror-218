#!/usr/bin/env python3
import logging
from time import time
from threading import Lock

from .exceptions import (
    KeyAlreadyExistsError,
    EntryNotFoundError,
    EntryExpiredError,
)

logger = logging.getLogger(__name__)


class CacheSettings:

    def __init__(self):
        self.error_on_dup_key = False
        self.error_on_invalid_key = False
        self.error_on_expired_entry = False
        self.default_ttl = 3600

    def get_settings(self):
        return vars(self)


class CacheController:

    def __init__(self):
        logger.info("Initializing SmoothCache")
        self._cache = {}
        self._lock = Lock()
        self.settings = CacheSettings()

    def set(self, key, value, ttl=None):
        """Add an entry to cache.

        :param key: Key to store the cache value under.
        :type key: str

        :param value: Value to cache
        :type value: Any

        :param ttl: Time-to-live value in seconds. Defaults to settings value.
        :type ttl: int
        """
        ttl = ttl if ttl is not None else self.settings.default_ttl

        if not isinstance(ttl, int):
            raise TypeError(f"Parameter 'ttl' must be an integer or 'None'")

        logger.info(f"Inserting cache entry '{key}' with {value} ({ttl=})")

        with self._lock:
            if self.settings.error_on_dup_key  \
                    and key in self._cache.keys():

                raise KeyAlreadyExistsError(
                    f"Cache with key '{key}' already exists in cache."
                )

            self._cache[key] = _CacheEntry(value, ttl)

        return

    def get(self, key, default=None):
        """Retreive an entry from the cache.

        Attempts to pull the provided key value from the cache. If the entry
        doesn't exist, this will return `default` OR raise an
        `EntryNotFoundError`, depending on the `error_on_invalid_key` cache
        setting. If the entry exists, there is a check to make sure the
        entry is within it's TTL. If the TTL has passes, this will return
        `default` OR raise an `EntryExpiredError`, depending on the
        `error_on_expired_entry` cache setting. Otherwise, we return a
        `CacheResult` object with the values in the cache.

        :param key: Key to retreive from the cache
        :type key: str

        :param default: The value to return if the key doesn't exist.
        :type default: Any

        :return: Cached value if it exists or `default`
        :rtype: CacheResult | Any

        :raises EntryNotFoundError: when key doesn't exist and
        error_on_invalid_key = True
        """
        try:
            with self._lock:
                cache_result = self._cache[key]

                if cache_result.expired:
                    logger.info(f"Cache miss for '{key}' - Entry expired")
                    del self._cache[key]

                    if self.settings.error_on_expired_entry:
                        raise EntryExpiredError(
                            f"Cache Entry '{key}' has expired."
                        )

                    return default

        except KeyError:
            logger.info(f"Cache miss for '{key}' - Entry not found")
            if self.settings.error_on_invalid_key:
                raise EntryNotFoundError(
                    f"No cache entry with key '{key}' found."
                )

            return default

        logger.info(f"Cache hit for '{key}'")
        return CacheResult(key=key, value=cache_result.value)

    def clear(self):
        """Remove all entries from cache."""
        logger.info("Clearing cache")
        with self._lock:
            self._cache = {}
        return

    def remove(self, key):
        """Remove the specified entry from the cache.

        :param key: Key of cache entry to remove.
        :type key: str
        """
        logger.info(f"Removing cache entry '{key}'")
        try:
            with self._lock:
                del self._cache[key]
        except KeyError:
            logger.warning(f"Could not remove entry '{key}' - Not found")
            if self.settings.error_on_invalid_key:
                raise EntryNotFoundError(
                    f"No cache entry with key '{key}' found."
                )
        return


class _CacheEntry:

    def __init__(self, value, ttl):
        self.value = value
        self.ttl = ttl
        self.created = time()

    @property
    def expired(self):
        """Whether the cache entry has expired."""
        return time() > (self.created + self.ttl)


class CacheResult:
    """Container for Cache Entries Results.

    :ivar key: The key of the cache entry returned
    :ivar value: The value of the cache entry returned
    """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"<CacheResult '{self.key}'>"
