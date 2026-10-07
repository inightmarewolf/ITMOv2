import unittest
from service import subscribe, subscribers, list_subscribers


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann")["subscribed"], True)
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaises(ValueError):
            subscribe(" ")

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)

    def test_list(self):
        subscribe("Bob")
        subscribe("Ann")
        self.assertEqual(list_subscribers(), ["Ann", "Bob"])


if __name__ == "__main__":
    unittest.main()
