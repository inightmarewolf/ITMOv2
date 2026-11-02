import unittest
from service import subscribe, subscribers, list_subscribers, unsubscribe


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann")["subscribed"], True)
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaises(ValueError) as ctx:
            subscribe(" ")
        self.assertEqual(str(ctx.exception), "empty name")

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)

    def test_list(self):
        subscribe("Bob")
        subscribe("Ann")
        self.assertEqual(list_subscribers(), ["Ann", "Bob"])


class UnsubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_unsubscribe(self):
        subscribe("Ann")
        self.assertEqual(unsubscribe("Ann"), {"unsubscribed": True, "name": "Ann"})
        self.assertEqual(list_subscribers(), [])

    def test_unsubscribe_trims(self):
        subscribe("Ann")
        self.assertEqual(unsubscribe("  Ann  ")["name"], "Ann")
        self.assertEqual(list_subscribers(), [])

    def test_unsubscribe_empty(self):
        subscribe("Ann")
        with self.assertRaises(ValueError) as ctx:
            unsubscribe(" ")
        self.assertEqual(str(ctx.exception), "empty name")
        self.assertEqual(list_subscribers(), ["Ann"])

    def test_unsubscribe_unknown(self):
        subscribe("Bob")
        with self.assertRaises(ValueError) as ctx:
            unsubscribe("Ann")
        self.assertEqual(str(ctx.exception), "unknown name")
        self.assertEqual(list_subscribers(), ["Bob"])


if __name__ == "__main__":
    unittest.main()
