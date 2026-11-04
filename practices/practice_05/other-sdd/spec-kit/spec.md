# Spec Kit — Feature Spec: unsubscribe-cli

> Прогон второго SDD-фреймворка на той же фиче. Код в итоге взят из OpenSpec-ветки; здесь фиксирую, как выглядел бы Spec Kit артефакт.

## User story

Как пользователь демо Notify Mini, я хочу снять подписку по имени через CLI, чтобы не перезапускать процесс.

## Acceptance

1. Given подписчик `Ann`, when `unsubscribe Ann`, then списка без `Ann` и exit 0.
2. Given пустой ввод, when unsubscribe, then `empty name` и набор не меняется.
3. Given нет имени, when unsubscribe, then `unknown name`.
4. Given только service API, when вызываю CLI `list`, then вижу отсортированные имена.

## Out of scope

Веб-UI, БД, case-insensitive имена, MCP-изменения.
