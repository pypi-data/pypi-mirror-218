# smoothcache

`smoothcache` is a simple, in-memory, thread-safe caching system for your python programs.

## Installation

```
pip install smoothcache
```

## Usage
On import, the library creates a global cache object named `Cache` that you can interact with.

``` python

from smoothcache import Cache

Cache.set("cache key", "cache value")

```

### Interacting with the cache object

The cache object exposes 4 methods for interacting with the cache:

 - set
 - get
 - clear
 - remove

#### Set

``` python
Cache.set(key, value, ttl=None)
```

The `set` method adds an entry to the cache.

The `key` parameter is how you can access the cached value.

The `ttl` parameter is the Time-to-Live value (in seconds) that the cache entry will remain valid.

After `ttl` seconds has passed, the cache will no longer return the value. The default ttl value is set at 3600 seconds (1 hour) and can be modified in the cache settings.

If a key is passed to `set` that already exists, the entry gets overridden. This behavior can be changed in the cache settings to instead raise a `KeyAlreadyExistsError` when a duplicate key is passed.

#### Get

``` python
Cache.get(key, default=None)
```

The `get` method retrieves an entry from the cache.

The `key` parameter is the value of the entries key set with the `set` method.

The `default` parameter is the value that will be returned if the entry is no longer valid, or doesn't exist.

`get` can also be configured in the cache settings to raise an `EntryNotFoundError` when the specified key doesn't exist or an `EntryExpiredError` when the specified cache entry has expired.

`get` returns a `CacheResult` object with two attributes (`key` and `value`) when the entry is found. Otherwise, `get` returns `default`.

#### Clear

``` python
Cache.clear()
```

The `clear` method removes all entries from the cache

#### Remove

``` python
Cache.remove(key)
```

The `remove` method removes the specified key from the cache.

By default, if the key doesn't exist in the cache, the function silently returns and doesn't fail. This behavior can be changed in the cache settings to instead raise an `EntryNotFoundError`.

### Cache Settings

The `Cache` object's behavior can be modified with it's settings. Settings are accessed within the object's `settings` property.

``` python
# Cache.settings.<setting name> = <setting value>
# For example:
Cache.settings.error_on_dup_key = False
```

`error_on_dup_key`:

__Default:__ False

If true, raise a `KeyAlreadyExistsError` when `set` is called with a `key` that is already set in the cache. If false, the cache entry with `key` is overwritten if the key is already set.

`error_on_invalid_key`:

__Default:__ False

If true, raise an `EntryNotFoundError` when `get` or `remove` is called with a `key` that is not set in the cache. If false, the `get` call will return it's default and the `remove` call silently returns.

`error_on_expired_entry`:

__Default:__ False

If true, raise an `EntryExpiredError` when the entry returned from a `get` call has gone past it's TTL. If false, the `get` call will return it's default.

`default_ttl`:

__Default:__ 3600 (1 hour)

The TTL value (in seconds) set on any entry that does not explicitly have a TTL value.
