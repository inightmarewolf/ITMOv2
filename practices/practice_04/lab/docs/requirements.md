# Контракт Notify Mini

## Фича A — валидация входа

- `subscribe(name)` отклоняет пустое имя и строку из пробелов.
- При отказе: `ValueError("empty name")`.
- Повторная подписка того же имени не создаёт дубликат.

## Фича B — список подписчиков

- `list_subscribers()` возвращает отсортированный список текущих имён.
- Данные только в памяти процесса (без persistence и CI).

## Фича C — отписка

- `unsubscribe(name)` снимает существующее имя после `.strip()`.
- Пустое имя → `ValueError("empty name")`.
- Неизвестное имя → `ValueError("unknown name")`.
- Успех → `{"unsubscribed": True, "name": <trimmed>}`.

## CLI

- `python cli.py subscribe|list|unsubscribe|help`
- Ошибки домена → exit 1; неизвестная команда / usage → exit 2.

## Проверка

```bash
make test
# или
python scripts/check.py
```
