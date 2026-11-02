# Proposal

## Why

В Notify Mini можно подписаться и посмотреть список, но нельзя снять подписку без перезапуска процесса. Для демо и сдачи ДЗ5 нужен понятный текстовый UI поверх той же логики, чтобы раздельно согласовать спеки экрана и API.

## What Changes

- Добавить `unsubscribe(name)` с теми же правилами нормализации имени, что у `subscribe`
- Добавить CLI (`cli.py`): команды `subscribe`, `list`, `unsubscribe`, `help`
- Сохранить поведение фич A/B без persistence и без новых зависимостей
- Расширить unit-тесты и прогнать через `make test`

## Capabilities

### New Capabilities

- `subscriber-lifecycle`: отписка по имени и инварианты набора подписчиков
- `notify-cli`: текстовый интерфейс команд поверх публичного API сервиса

### Modified Capabilities

_(нет — main specs ещё пустые до первого archive)_

## Impact

- Код: `service.py`, новый `cli.py`, `test_service.py`, при необходимости `test_cli.py`
- Документы: `docs/requirements.md`, `FEATURES.md`, `AGENTS.md`
- Проверка: `python scripts/check.py` / `make test`
