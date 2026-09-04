import unittest

from orderlib import normalize_orders


class NormalizerPublicTests(unittest.TestCase):
    def test_simple_record(self) -> None:
        records = [{"order_id": "B-2", "currency": " usd ", "amount": "12"}]
        self.assertEqual(
            normalize_orders(records),
            [{"order_id": "B-2", "currency": "USD", "amount": "12.00"}],
        )


if __name__ == "__main__":
    unittest.main()
