"""Сквозное демо CLI в одном процессе (in-memory set иначе пустеет между запусками)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli import main  # noqa: E402
from service import subscribers  # noqa: E402


def step(argv: list[str]) -> None:
    print(f"$ python cli.py {' '.join(argv)}")
    code = main(argv)
    print(f"exit={code}")
    print("---")


def run() -> int:
    subscribers.clear()
    step(["help"])
    step(["subscribe", "Ann"])
    step(["subscribe", "Bob"])
    step(["list"])
    step(["unsubscribe", "Ann"])
    step(["list"])
    step(["unsubscribe", "Ghost"])
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
