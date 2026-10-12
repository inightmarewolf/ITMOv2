---
name: notify-tests
description: TDD-чек для Notify Mini — прогон unittest после правок subscribe/list_subscribers и разбор типичных падений
---

# Skill: notify-tests

Используй при любых правках `service.py` или тестов (фичи A и B).

## Процедура

1. Прочитай `docs/requirements.md`.
2. Запусти runner: `python scripts/check.py` (или `make test`).
3. Если красный:
   - `test_empty` → пустое/`" "` должно давать `ValueError("empty name")` (фича A).
   - `test_list` → `list_subscribers()` возвращает отсортированный список (фича B).
   - `test_duplicate` → повтор `subscribe` не увеличивает множество.
4. Для ручной проверки домена вызови MCP tool `subscribe_name`.
5. Сообщи: сколько тестов, что упало, что сделаешь дальше.

Не утверждай «тесты зелёные», если runner не запускался.
