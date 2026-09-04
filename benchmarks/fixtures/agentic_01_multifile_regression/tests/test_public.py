import unittest

from cachelib import HTTPCache


class HTTPCachePublicTests(unittest.TestCase):
    def test_fresh_value_is_returned(self) -> None:
        cache = HTTPCache()
        self.assertTrue(cache.put("user:1", {"name": "Ana"}, "max-age=60", 100.0))
        self.assertEqual(cache.get("user:1", 120.0), {"name": "Ana"})

    def test_missing_key_returns_none(self) -> None:
        self.assertIsNone(HTTPCache().get("missing", 100.0))


if __name__ == "__main__":
    unittest.main()
