# Часть 2 занятия — правило OpenSpec и форма design до/после

В `practice_04/lab/openspec/config.yaml` добавлены rules, в т.ч.:

```yaml
rules:
  design:
    - Объясни взаимодействие диаграммой Mermaid.
    - Явно перечисли Non-Goals, чтобы агент не расползался.
```

## Фрагмент design ДО правила

Раньше в черновике было просто:

> CLI вызывает service.unsubscribe и печатает результат.

Без диаграммы и без Non-Goals — агенту легко додумать «давайте сразу prompt-loop и цвета».

## Фрагмент design ПОСЛЕ правила

В `openspec/changes/archive/2026-10-29-unsubscribe-cli/design.md` уже есть Non-Goals и Mermaid sequenceDiagram (User → cli.py → service.py). Смысл тот же, форма жёстче: границы и взаимодействие видны до apply.
