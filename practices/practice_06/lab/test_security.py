"""Регрессии по дырам HW6. На уязвимом сервисе часть сценариев была бы открыта."""

import unittest

from service import Shop


class SecurityRegressionTest(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.addCleanup(self.shop.close)

    def request(self, method, path, body=None, headers=None):
        with self.shop.lock:
            return self.shop.dispatch(method, path, body or {}, headers or {})

    def login(self, username="alice", password="learn-alice"):
        status, result = self.request("POST", "/login", {"username": username, "password": password})
        self.assertEqual(status, 200)
        return {"X-Token": result["token"]}

    def test_profile_idor_blocked(self):
        auth = self.login()
        status, body = self.request("GET", "/profile?id=2", headers=auth)
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "forbidden")

    def test_sql_injection_profile_id_safe(self):
        auth = self.login()
        status, body = self.request("GET", "/profile?id=1 OR 1=1", headers=auth)
        self.assertEqual(status, 400)

    def test_search_not_public(self):
        self.assertEqual(self.request("GET", "/search?q=TEST")[0], 401)
        self.assertEqual(self.request("GET", "/search?q=TEST", headers=self.login())[0], 403)

    def test_orders_not_leaked_across_users(self):
        alice = self.login()
        status, orders = self.request("GET", "/orders", headers=alice)
        self.assertEqual(status, 200)
        self.assertTrue(all(o["owner"] == 1 for o in orders))

    def test_client_price_ignored(self):
        status, order = self.request(
            "POST", "/orders", {"product": "lamp", "price": 1}, self.login()
        )
        self.assertEqual(status, 201)
        self.assertEqual(order["price"], 1500)

    def test_admin_export_ignores_spoofed_role_header(self):
        auth = {**self.login(), "X-Role": "staff"}
        self.assertEqual(self.request("GET", "/admin/export", headers=auth)[0], 403)
        staff = self.login("staff", "learn-staff")
        self.assertEqual(self.request("GET", "/admin/export", headers=staff)[0], 200)

    def test_files_foreign_receipt_blocked(self):
        auth = self.login()
        status, _ = self.request("GET", "/files?user=bob&path=receipt.txt", headers=auth)
        self.assertEqual(status, 403)

    def test_private_note_not_via_files(self):
        auth = self.login()
        # path вне files/<me>/receipt.txt
        status, _ = self.request("GET", "/files?user=alice&path=../private/operator-note.txt", headers=auth)
        self.assertEqual(status, 403)

    def test_debug_logs_staff_only_and_redacted(self):
        self.assertEqual(self.request("GET", "/debug/logs")[0], 401)
        self.login()
        staff = self.login("staff", "learn-staff")
        status, logs = self.request("GET", "/debug/logs", headers=staff)
        self.assertEqual(status, 200)
        blob = str(logs)
        self.assertNotIn("learn-alice", blob)
        self.assertIn("<redacted>", blob)

    def test_review_xss_escaped(self):
        auth = self.login()
        payload = "<script>alert(1)</script>"
        self.assertEqual(
            self.request("POST", "/reviews", {"product": "chair", "text": payload}, auth)[0],
            201,
        )
        html_page = self.request("GET", "/reviews/view", headers=auth)[1]
        self.assertNotIn("<script>", html_page)
        self.assertIn("&lt;script&gt;", html_page)

    def test_assistant_blocks_foreign_order_context(self):
        auth = self.login()
        self.assertEqual(self.request("GET", "/assistant/context?order_id=2", headers=auth)[0], 403)

    def test_assistant_execute_refuses_delete_and_export(self):
        auth = self.login()
        self.assertEqual(
            self.request(
                "POST",
                "/assistant/execute",
                {"decision": {"tool": "delete_tree", "arguments": {"path": "."}}},
                auth,
            )[0],
            403,
        )
        self.assertEqual(
            self.request(
                "POST",
                "/assistant/execute",
                {"decision": {"tool": "export_profiles", "arguments": {}}},
                auth,
            )[0],
            403,
        )

    def test_assistant_execute_blocks_foreign_receipt(self):
        auth = self.login()
        status, _ = self.request(
            "POST",
            "/assistant/execute",
            {"decision": {"tool": "read_file", "arguments": {"path": "files/bob/receipt.txt"}}},
            auth,
        )
        self.assertEqual(status, 403)

    def test_assistant_execute_allows_own_receipt(self):
        auth = self.login()
        status, result = self.request(
            "POST",
            "/assistant/execute",
            {"decision": {"tool": "read_file", "arguments": {"path": "files/alice/receipt.txt"}}},
            auth,
        )
        self.assertEqual(status, 200)
        self.assertIn("TEST_ALICE", result["content"])


if __name__ == "__main__":
    unittest.main()
