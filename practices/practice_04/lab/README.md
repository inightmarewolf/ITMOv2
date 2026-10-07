# Практика 4 — Notify Mini (среда агента)

## Фичи

См. `FEATURES.md`: **A** валидация имени, **B** список подписчиков.

## Среда

| Компонент | Зачем |
|---|---|
| `AGENTS.md` | куда смотреть, команды, ограничения |
| skill `notify-tests` | процедура прогона тестов после правок |
| MCP `subscribe_name` | доменный tool + ошибка на пустом имени |
| hook `check-after-edit` | после edit `.py` гоняет `scripts/check.py` |
| runner | `python scripts/check.py` / `make test` |

## Быстрый старт

```bash
cd practices/practice_04/lab
make test
make selfcheck
# нужен VSELLM_API_KEY
opencode
```

Промпт для демо:

```
Прочитай AGENTS.md и docs/requirements.md.
Загрузи skill notify-tests.
Вызови MCP subscribe_name с name=Ann и с пустым именем.
Покажи результаты. Код пока не меняй.
```

## Сдача

- файлы среды + MCP + skill + hook
- `evidence/` — подтверждения
- `reflection.md`
- презентация: `practices/submit.html`
