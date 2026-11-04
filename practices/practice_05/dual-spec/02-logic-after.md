# Команда 2 — спека логики (ПОСЛЕ контракта)

## Данные

- Тот же `subscribers: set[str]`
- Имена хранятся как после `.strip()`, регистр сохраняется

## API

```
unsubscribe(name: str) -> {"unsubscribed": True, "name": str}
```

## Правила

1. `cleaned = name.strip()`
2. Пустой `cleaned` → `ValueError("empty name")`
3. `cleaned not in subscribers` → `ValueError("unknown name")`
4. Иначе `remove` и вернуть dict
5. Без `.lower()`, без persistence, без HTTP

## Совместимость

Поведение `subscribe` / `list_subscribers` не меняется.
