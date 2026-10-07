# REPORT — Практика 3: локальные модели и OpenCode

## Железо

| Параметр | Значение |
|---|---|
| CPU | 11th Gen Intel Core i5-11400F @ 2.60GHz |
| RAM | 16 GB |
| GPU | NVIDIA GeForce GTX 1060 3GB |
| ОС | Windows 10 (x64), работа без WSL |

## Софт

| Компонент | Версия |
|---|---|
| Ollama | 0.40.0 |
| OpenCode | 1.18.35 |
| Python | 3.14.3 |
| Make | GNU Make 4.4.1 (Windows) |

## Модель и обоснование выбора

| Поле | Значение |
|---|---|
| База | `qwen3.5:4b` |
| Кастомные теги | `itmo` (чат), `itmo-agent` (агент) |
| Параметры | ~4.7B |
| Квантизация | Q4_K_M (~3.4 GB) |
| `num_ctx` | 4096 (`itmo`), 8192 (`itmo-agent`) |
| `temperature` | 0.2 |
| `seed` | 42 |

**Почему:** 0.8B слишком слаба для ответов по коду; 4B Q4_K_M помещается в 3 GB VRAM + системную RAM. Контекст агента снижен до 8192: при 65536 на GTX 1060 3GB Ollama уходила почти полностью на CPU (~87%) и отвечала очень медленно. Temperature 0.2 и seed 42 — для более стабильных ответов на фактические вопросы.

## Modelfile

Изменения относительно шаблона курса:

- `PARAMETER seed 42` в обоих файлах;
- в `Modelfile` добавлено требование указывать файл и строку.

Сборка:

```bash
ollama create itmo -f Modelfile
ollama create itmo-agent -f Modelfile.agent
```

## OpenCode (`demo/opencode.json`)

Настроено взаимодействие с локальной Ollama по OpenAI-compatible API:

- `baseURL`: `http://localhost:11434/v1`
- модели `ollama/itmo-agent` и `ollama/itmo`
- агент `local-guide`: prompt из `repo-system.txt`, права только на чтение (`read` / `glob` / `grep` / `list`)
- `default_agent`: `local-guide`

Запуск из `lab/demo/`: `opencode` (выбрать `ollama/itmo-agent`).

## `make test`

На Windows в Makefile заменён `python3` → `python` (Error 9009). Результат:

```
Ran 3 tests in 0.000s
OK
```

## Пять вопросов (`QUESTIONS.md`)

Эталоны: `ETALONS.md` (тестовой модели не передавались).  
Сырые ответы: `results/Q01.txt` … `Q05.txt`, журнал: `results/RUNLOG.md`.  
Запуск: отдельные сессии локальной модели `itmo-agent` (Ollama API `http://localhost:11434`, агент/конфиг `demo/opencode.json`, read-only).

| Q | Эталон (кратко) | Ответ модели | Оценка |
|---|---|---|---|
| 1 | `make test`, источник Makefile/README | `make test` в Makefile, строка 2 | **верно** |
| 2 | `ValueError("empty name")` при пустом имени | верно, `service.py` строка 6 | **верно** |
| 3 | ложная предпосылка, unsubscribe нет | явно: реализации нет, предпосылка неверна | **верно** |
| 4 | сведений о CI нет | «Сведений о CI-системе в файлах нет» | **верно** |
| 5 | нет, `subscribers = set()` в памяти | нет, ссылка на `service.py:1` | **верно** |

Время ответов: ~3–18 с на вопрос (суммарно ~65 с на пять запусков).

## Ограничения и выводы

1. На Windows курсный `python3` в Makefile ломает `make test` — нужна правка или WSL.
2. Локальная 4B с жёстким system prompt хорошо держит «нет данных» (CI) и ложную предпосылку (unsubscribe), почти без галлюцинаций на этом маленьком репо.
3. Контекст 64k в `itmo-agent` на GTX 1060 3GB уводил инференс на CPU; рабочий `num_ctx 8192` заметно быстрее и достаточен для `demo/`.
4. OpenCode + Ollama (`/v1`) работают локально; узкое место — VRAM и скорость 4B, не сам сетап провайдера.
