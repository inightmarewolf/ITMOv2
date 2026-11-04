import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

import cli
from service import subscribers, subscribe


class CliTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def _run(self, argv):
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_help(self):
        code, out, err = self._run(["help"])
        self.assertEqual(code, 0)
        self.assertIn("subscribe", out)
        self.assertEqual(err, "")

    def test_subscribe_and_list(self):
        code, out, _ = self._run(["subscribe", "Ann"])
        self.assertEqual(code, 0)
        self.assertIn("Ann", out)
        code, out, _ = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "Ann")

    def test_unsubscribe_ok(self):
        subscribe("Ann")
        code, out, err = self._run(["unsubscribe", "Ann"])
        self.assertEqual(code, 0)
        self.assertIn("unsubscribed Ann", out)
        self.assertEqual(err, "")

    def test_unsubscribe_unknown(self):
        code, out, err = self._run(["unsubscribe", "Ghost"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("unknown name", err)

    def test_unknown_command(self):
        code, out, err = self._run(["bounce", "Ann"])
        self.assertEqual(code, 2)
        self.assertIn("unknown command", err)


if __name__ == "__main__":
    unittest.main()
