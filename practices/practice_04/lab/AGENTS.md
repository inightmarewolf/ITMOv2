# AGENTS.md — Notify Mini

Короткий навигатор. Детали — в `docs/`.

## Фичи

- **A:** валидация пустого имени в `subscribe`
- **B:** `list_subscribers()` — отсортированный список

## Куда смотреть

| Что | Путь |
|---|---|
| Контракт | `docs/requirements.md` |
| Style guide | `docs/style-guide.md` |
| Код | `service.py` |
| Тесты | `test_service.py` |
| Skill | `.opencode/skills/notify-tests/SKILL.md` |
| MCP tool | `subscribe_name` (сервер `notify`) |
| Hook | `.opencode/plugins/check-after-edit.js` |
| Runner | `python scripts/check.py` или `make test` |

## Правила

1. Перед правкой прочитай `docs/requirements.md` и `docs/style-guide.md`.
2. Загрузи skill `notify-tests`.
3. Для проверки подписки вызывай MCP `subscribe_name`.
4. После edit дождись результата hook/runner.
5. Не выдумывай persistence и CI.
6. Не делай commit без явной просьбы.
