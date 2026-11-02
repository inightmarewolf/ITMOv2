"""Текстовый UI для Notify Mini."""
from __future__ import annotations

import sys

from service import list_subscribers, subscribe, unsubscribe


HELP = """Notify Mini CLI
Commands:
  subscribe <name>
  list
  unsubscribe <name>
  help
"""


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"help", "-h", "--help"}:
        print(HELP.strip())
        return 0

    command = args[0]
    try:
        if command == "subscribe":
            if len(args) < 2:
                print("usage: subscribe <name>", file=sys.stderr)
                return 2
            result = subscribe(args[1])
            print(f"subscribed {result['name']}")
            return 0

        if command == "list":
            names = list_subscribers()
            if not names:
                print("(empty)")
            else:
                print("\n".join(names))
            return 0

        if command == "unsubscribe":
            if len(args) < 2:
                print("usage: unsubscribe <name>", file=sys.stderr)
                return 2
            result = unsubscribe(args[1])
            print(f"unsubscribed {result['name']}")
            return 0

        print(f"unknown command: {command}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
