"""Local shop exercise. Identities and data are synthetic. Hardened for HW6."""

from __future__ import annotations

import argparse
import html
import json
import re
import sqlite3
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from sandbox import Sandbox

OWN_RECEIPT = re.compile(r"^files/([a-z]+)/receipt\.txt$")


class Shop:
    def __init__(self):
        self.sandbox = Sandbox()
        self.lock = threading.RLock()
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE profiles(id INTEGER PRIMARY KEY, name TEXT, email TEXT, address TEXT);
            INSERT INTO profiles VALUES
                (1, 'TEST_ALICE', 'alice@example.invalid', 'TEST_ADDRESS_A'),
                (2, 'TEST_BOB', 'bob@example.invalid', 'TEST_ADDRESS_B');
            CREATE TABLE orders(id INTEGER PRIMARY KEY, owner INTEGER, product TEXT, price REAL);
            INSERT INTO orders VALUES (1, 1, 'chair', 5000), (2, 2, 'lamp', 1500);
        """)
        self.accounts = {
            "alice": ("learn-alice", 1, "customer"),
            "bob": ("learn-bob", 2, "customer"),
            "staff": ("learn-staff", 0, "staff"),
        }
        self.id_to_user = {1: "alice", 2: "bob"}
        self.sessions = {}
        self.products = {"chair": 5000, "lamp": 1500}
        self.reviews = []
        self.logs = []

    def rows(self, query, params=()):
        return [dict(row) for row in self.db.execute(query, params)]

    def session(self, headers):
        token = headers.get("X-Token")
        if not token:
            return None
        return self.sessions.get(token)

    def require_login(self, headers):
        session = self.session(headers)
        if not session:
            return None, (401, {"error": "login required"})
        return session, None

    def require_staff(self, headers):
        session, err = self.require_login(headers)
        if err:
            return None, err
        if session["role"] != "staff":
            return None, (403, {"error": "staff only"})
        return session, None

    def redact_log(self, method, target, body, headers):
        safe_headers = {
            k: ("<redacted>" if k.lower() in {"x-token", "authorization"} else v)
            for k, v in dict(headers).items()
        }
        safe_body = dict(body) if isinstance(body, dict) else {}
        if "password" in safe_body:
            safe_body["password"] = "<redacted>"
        return {"method": method, "target": target, "body": safe_body, "headers": safe_headers}

    def own_receipt_path(self, session):
        username = session.get("username")
        if not username or username not in {"alice", "bob"}:
            return None
        return f"files/{username}/receipt.txt"

    def dispatch(self, method, target, body, headers):
        url = urlsplit(target)
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        self.logs.append(self.redact_log(method, target, body, headers))

        if method == "GET" and url.path == "/health":
            return 200, {"status": "ok"}
        if method == "GET" and url.path == "/products":
            return 200, self.products

        if method == "POST" and url.path == "/login":
            username = body.get("username")
            account = self.accounts.get(username)
            if not account or body.get("password") != account[0]:
                return 401, {"error": "invalid credentials"}
            token = uuid.uuid4().hex
            self.sessions[token] = {
                "id": account[1],
                "role": account[2],
                "username": username,
            }
            return 200, {"token": token}

        if method == "GET" and url.path == "/profile":
            session, err = self.require_login(headers)
            if err:
                return err
            try:
                requested = int(query.get("id", session["id"]))
            except (TypeError, ValueError):
                return 400, {"error": "bad id"}
            if session["role"] != "staff" and requested != session["id"]:
                return 403, {"error": "forbidden"}
            return 200, self.rows("SELECT * FROM profiles WHERE id = ?", (requested,))

        if method == "GET" and url.path == "/search":
            session, err = self.require_staff(headers)
            if err:
                return err
            needle = query.get("q", "")
            return 200, self.rows(
                "SELECT * FROM profiles WHERE name LIKE ?",
                (f"%{needle}%",),
            )

        if method == "GET" and url.path == "/orders":
            session, err = self.require_login(headers)
            if err:
                return err
            if session["role"] == "staff":
                return 200, self.rows("SELECT * FROM orders")
            return 200, self.rows("SELECT * FROM orders WHERE owner = ?", (session["id"],))

        if method == "POST" and url.path == "/orders":
            session, err = self.require_login(headers)
            if err:
                return err
            product = body.get("product")
            if product not in self.products:
                return 400, {"error": "unknown product"}
            # цена только из каталога — клиентский price игнорируем
            price = self.products[product]
            cursor = self.db.execute(
                "INSERT INTO orders(owner, product, price) VALUES (?, ?, ?)",
                (session["id"], product, price),
            )
            self.db.commit()
            return 201, {
                "id": cursor.lastrowid,
                "owner": session["id"],
                "product": product,
                "price": price,
            }

        if method == "GET" and url.path == "/admin/export":
            session, err = self.require_staff(headers)
            if err:
                return err
            return 200, self.rows("SELECT * FROM profiles")

        if method == "GET" and url.path == "/files":
            session, err = self.require_login(headers)
            if err:
                return err
            user = query.get("user", "")
            path = query.get("path", "receipt.txt")
            if session["role"] != "staff":
                if user != session["username"] or path != "receipt.txt":
                    return 403, {"error": "forbidden"}
            name = f"files/{user}/{path}"
            try:
                return 200, {"content": self.sandbox.read(name)}
            except (ValueError, FileNotFoundError, IsADirectoryError, OSError) as exc:
                return 404, {"error": str(exc)}

        if method == "GET" and url.path == "/debug/logs":
            session, err = self.require_staff(headers)
            if err:
                return err
            return 200, self.logs.copy()

        if method == "POST" and url.path == "/reviews":
            session, err = self.require_login(headers)
            if err:
                return err
            product = body.get("product")
            text = body.get("text", "")
            if product not in self.products:
                return 400, {"error": "unknown product"}
            if not isinstance(text, str) or not text.strip():
                return 400, {"error": "empty review"}
            self.reviews.append({"product": product, "text": text, "author": session["username"]})
            return 201, {"saved": True}

        if method == "GET" and url.path == "/reviews/view":
            parts = "".join(f"<p>{html.escape(r['text'])}</p>" for r in self.reviews)
            return 200, f"<html><body>{parts}</body></html>"

        if method == "GET" and url.path == "/assistant/context":
            session, err = self.require_login(headers)
            if err:
                return err
            try:
                order_id = int(query.get("order_id", "0"))
            except (TypeError, ValueError):
                return 400, {"error": "bad order_id"}
            orders = self.rows("SELECT * FROM orders WHERE id = ?", (order_id,))
            if not orders:
                return 404, {"error": "order not found"}
            if session["role"] != "staff" and orders[0]["owner"] != session["id"]:
                return 403, {"error": "forbidden"}
            safe_reviews = [
                {"product": r["product"], "text": r["text"][:200]}
                for r in self.reviews
                if r.get("author") == session["username"]
            ]
            prompt = (
                "Ты помощник магазина. Верни только JSON с полями tool и arguments.\n"
                "Разрешён один инструмент для клиента: read_file(path) — только свой чек.\n"
                "Запрещены: export_profiles, delete_tree, чужие файлы. При сомнении tool=refuse.\n"
                f"Заказ: {json.dumps(orders, ensure_ascii=False)}\n"
                f"Свои отзывы: {json.dumps(safe_reviews, ensure_ascii=False)}\n"
                f"Запрос пользователя: {query.get('question', 'Покажи чек по заказу')}"
            )
            return 200, {"prompt": prompt}

        if method == "POST" and url.path == "/assistant/execute":
            session, err = self.require_login(headers)
            if err:
                return err
            decision = body.get("decision") or {}
            tool = decision.get("tool")
            arguments = decision.get("arguments") or {}
            if tool == "refuse":
                return 200, {"refused": True, "reason": arguments.get("reason", "refused")}
            if tool == "read_file":
                path = arguments.get("path", "")
                allowed = self.own_receipt_path(session)
                if session["role"] != "staff" and path != allowed:
                    return 403, {"error": "forbidden path"}
                match = OWN_RECEIPT.match(path or "")
                if not match:
                    return 403, {"error": "forbidden path"}
                try:
                    return 200, {"content": self.sandbox.read(path)}
                except (ValueError, FileNotFoundError, OSError) as exc:
                    return 404, {"error": str(exc)}
            # опасные инструменты отключаем на сервере независимо от модели
            if tool in {"export_profiles", "delete_tree"}:
                return 403, {"error": "tool not allowed"}
            return 400, {"error": "unknown tool"}

        return 404, {"error": "not found"}

    def close(self):
        self.db.close()
        self.sandbox.close()


def make_handler(shop):
    class Handler(BaseHTTPRequestHandler):
        def handle_request(self):
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 <= size <= 65536:
                    self.send_error(413)
                    return
                body = json.loads(self.rfile.read(size)) if size else {}
                with shop.lock:
                    status, result = shop.dispatch(self.command, self.path, body, self.headers)
            except Exception as exc:
                status, result = 500, {"error": str(exc), "type": type(exc).__name__}
            html_resp = isinstance(result, str)
            data = (result if html_resp else json.dumps(result, ensure_ascii=False)).encode("utf-8")
            self.send_response(status)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8" if html_resp else "application/json; charset=utf-8",
            )
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_GET = do_POST = handle_request

        def log_message(self, format, *args):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8066)
    args = parser.parse_args()
    shop = Shop()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(shop))
    server.daemon_threads = True
    print(f"Local exercise: http://127.0.0.1:{server.server_port}", flush=True)
    print(f"Disposable fixture files: {shop.sandbox.root}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        shop.close()


if __name__ == "__main__":
    main()
