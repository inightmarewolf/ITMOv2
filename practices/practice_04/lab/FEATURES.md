# Какие фичи берём

Учебный проект **Notify Mini** (сервис подписки), не большой сквозной проект курса.

| Фича | Суть | Где |
|---|---|---|
| **A** | Валидация входа: пустое имя → `ValueError("empty name")` | `service.subscribe`, `test_empty` |
| **B** | Список подписчиков: `list_subscribers()` отсортирован | `service.list_subscribers`, `test_list` |
| **C** | Отписка: `unsubscribe(name)` + CLI | `service.unsubscribe`, `cli.py`, `test_cli` |

На семинаре A/B делали в worktree; для ДЗ4 достаточно среды агента + A/B.
Фича C — практика/ДЗ 5 (OpenSpec + dual-spec UI/логика).
