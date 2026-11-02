# Общий контракт (после сверки двух спек)

Разбирали расхождения в двух чатах / двух документах. Ниже принятые решения человека.

## Расхождения → решения

| Тема | UI хотела | Логика хотела | Итог |
|---|---|---|---|
| Интерфейс | TUI со стрелками и цветом | только функции сервиса | **Простой argv-CLI**, без curses/цвета (style guide: stdlib, без расползания) |
| Сигнатура | «endpoint удаления» | `unsubscribe -> bool` | **`unsubscribe(name) -> dict`**, ошибки через `ValueError` как у `subscribe` |
| Пустое имя | отдельное сообщение | `False` | **`ValueError("empty name")`** — единообразие с фичей A |
| Нет имени | сообщение, меню живо | `False` | **`ValueError("unknown name")`**, CLI печатает текст и exit 1 |
| Регистр | не обсуждали | `.lower()` | **Без lower**: `subscribe` уже case-sensitive, менять A/B нельзя в этом change |

## Контракт данных / вызовов

```
subscribe(name) -> {"subscribed": True, "name": trimmed}
unsubscribe(name) -> {"unsubscribed": True, "name": trimmed}
list_subscribers() -> list[str]  # sorted

CLI:
  python cli.py subscribe <name>     # exit 0 | 1
  python cli.py list                 # exit 0
  python cli.py unsubscribe <name>   # exit 0 | 1
  python cli.py help                 # exit 0
  unknown command / usage            # exit 2
```

## Состояния UI (упрощённые)

Только: показ help → выполнениеда → успех в stdout / ошибка в stderr. Отдельного `menu_select` нет.

## Что обновить в спеках

Обе стороны правят свои документы под этот контракт (см. `*-after.md`), потом реализация.
