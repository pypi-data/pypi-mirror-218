#!/usr/bin/env python3
import unittest
import smoothcache


class TestSmoothCacheSet(unittest.TestCase):

    def setUp(self):
        self.cache = smoothcache.CacheController()

    def tearDown(self):
        self.cache = None

    def test_set(self):
        self.cache.set("test key", "test value")

        self.assertEqual(len(self.cache._cache), 1)
        self.assertEqual(self.cache._cache["test key"].value, "test value")

    def test_set_override(self):
        self.cache.set("test key", "original value")
        self.cache.set("test key", "new value")

        self.assertEqual(len(self.cache._cache), 1)
        self.assertEqual(self.cache._cache["test key"].value, "new value")

    def test_set_override_exception(self):
        self.cache.settings.error_on_dup_key = True

        self.cache.set("test key", "original value")

        with self.assertRaises(smoothcache.KeyAlreadyExistsError):
            self.cache.set("test key", "new value")

        self.assertEqual(self.cache._cache["test key"].value, "original value")

    def test_set_default_ttl(self):
        self.cache.set("test key", "test value")

        self.assertEqual(
            self.cache._cache["test key"].ttl,
            self.cache.settings.default_ttl
        )

        self.cache.settings.default_ttl = 60
        self.cache.set("test key", "test value")

        self.assertEqual(
            self.cache._cache["test key"].ttl,
            60
        )

    def test_set_custom_ttl(self):
        self.cache.set("test key", "test_value", ttl=59)

        self.assertEqual(
            self.cache._cache["test key"].ttl,
            59
        )


class TestSmoothCacheClear(unittest.TestCase):

    def setUp(self):
        self.cache = smoothcache.CacheController()

    def tearDown(self):
        self.cache = None

    def test_clear_cache(self):
        self.cache.set("test key", "test value")
        self.cache.set("test key 2", "test value 2")

        self.cache.clear()

        self.assertEqual(len(self.cache._cache), 0)


class TestSmoothCacheGet(unittest.TestCase):

    def setUp(self):
        self.cache = smoothcache.CacheController()
        self.cache.set("test key", "test value")

    def tearDown(self):
        self.cache = None

    def test_get(self):
        res = self.cache.get("test key")

        self.assertIsInstance(res, smoothcache.smooth.CacheResult)
        self.assertEqual(res.key, "test key")
        self.assertEqual(res.value, "test value")

    def test_get_default(self):
        res = self.cache.get("does not exist")

        self.assertIsNone(res)

        res = self.cache.get("does not exist", default="Not found")
        self.assertEqual(res, "Not found")

    def test_get_not_found_error(self):
        self.cache.settings.error_on_invalid_key = True

        with self.assertRaises(smoothcache.EntryNotFoundError):
            res = self.cache.get("does not exist")

    def test_get_expired_entry(self):
        self.cache.set("expired", "expired value", ttl=-1)

        res = self.cache.get("expired")

        self.assertNotIsInstance(res, smoothcache.smooth.CacheResult)
        self.assertIsNone(res)
        # Entry should be deleted, we still should have the entry from `setUp`
        self.assertEqual(len(self.cache._cache), 1)

    def test_get_custom_default_expired_entry(self):
        self.cache.set("expired", "expired value", ttl=-1)

        res = self.cache.get("expired", default="Not found")

        self.assertNotIsInstance(res, smoothcache.smooth.CacheResult)
        self.assertEqual(res, "Not found")

        # Entry should be deleted, we still should have the entry from `setUp`
        self.assertEqual(len(self.cache._cache), 1)

    def test_get_expired_entry_error(self):
        self.cache.settings.error_on_expired_entry = True

        self.cache.set("expired", "expired_value", ttl=-1)

        with self.assertRaises(smoothcache.EntryExpiredError):
            self.cache.get("expired")

        # Entry should be deleted, we still should have the entry from `setUp`
        self.assertEqual(len(self.cache._cache), 1)


class TestSmoothCacheRemove(unittest.TestCase):

    def setUp(self):
        self.cache = smoothcache.CacheController()
        self.cache.set("test key", "test value")
        self.cache.set("test key 2", "test value 2")

    def tearDown(self):
        self.cache = None

    def test_remove(self):
        self.cache.remove("test key")
        self.assertEqual(len(self.cache._cache), 1)
        self.cache.remove("test key 2")
        self.assertEqual(len(self.cache._cache), 0)

    def test_remove_not_found(self):
        with self.assertLogs('smoothcache.smooth', level="WARNING") as logs:
            self.cache.remove("does not exist")
        self.assertIn(
            "WARNING:smoothcache.smooth:Could not remove entry "
            + "'does not exist' - Not found",
            logs.output
        )
        self.assertEqual(len(self.cache._cache), 2)

    def test_remove_not_found_exception(self):
        self.cache.settings.error_on_invalid_key = True

        with self.assertRaises(smoothcache.EntryNotFoundError), \
                self.assertLogs("smoothcache.smooth", level="WARNING") as logs:
            self.cache.remove("does not exist")

        self.assertIn(
            "WARNING:smoothcache.smooth:Could not remove entry "
            + "'does not exist' - Not found",
            logs.output
        )

        self.assertEqual(len(self.cache._cache), 2)


if __name__ == "__main__":
    unittest.main()
