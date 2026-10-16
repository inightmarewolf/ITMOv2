# HANDOFF — Практика 4 / Notify Mini

## Сделано

- Фича A: валидация пустого имени.
- Фича B: `list_subscribers()`.
- Среда: `AGENTS.md`, skill `notify-tests`, MCP `subscribe_name`, hook `check-after-edit`, runner `scripts/check.py`.
- Evidence: `evidence/`, рефлексия `reflection.md`, обзор `practices/submit.html`.

## Как проверить

```bash
make test
make selfcheck
```

## Ограничения

- Без persistence и CI.
- OpenCode студента: 1.18.x (не 2.0.20 из презентации) — hook в формате `tool.execute.after`.
- Рабочий агент для демо среды: VseLLM, не локальная 4B.
