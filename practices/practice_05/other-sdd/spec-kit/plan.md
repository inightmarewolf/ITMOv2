# Spec Kit — Plan

## Approach

1. Расширить `service.py` функцией `unsubscribe`.
2. Добавить `cli.py` как argparse-подобный разбор argv.
3. Юнит-тесты на service + cli.
4. Обновить requirements/FEATURES.

## Technical constraints

- Сохранить публичные контракты A/B.
- Не добавлять зависимости в requirements.

## Test plan

- `make test` — unittest discovery
- Ручной прогон трёх CLI-команд подряд
