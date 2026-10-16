# Skill `notify-tests` — устройство и запуск

## Устройство (свои слова)

Skill лежит в `.opencode/skills/notify-tests/`. В frontmatter заданы `name` и `description`, чтобы OpenCode находил его через tool `skill`. В теле — пошаговая автоматизация: прочитать контракт, запустить `python scripts/check.py`, разобрать типичные падения `test_empty` / `test_list`, при необходимости вызвать MCP. Рядом reference `writing-good-tests.md` с короткими правилами тестов. Skill сам код не исполняет — он заставляет агента идти через runner, а не «обещать» зелёные тесты.

## Проверенный результат runner

```text
$ python scripts/check.py
test_duplicate ... ok
test_empty ... ok
test_list ... ok
test_subscribe ... ok
Ran 4 tests in 0.000s
OK
```

Дата фиксации: прогон в lab после сборки фич A/B.
