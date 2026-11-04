# Отчёт 2. Повторные проверки после исправлений

Правки только в `lab/service.py` (+ тесты). `sandbox.py` не менял.

## Что изменилось по пунктам

| Было | Стало | Повторная проверка |
|---|---|---|
| SQL склейка | `?` placeholders + валидация id | `test_sql_injection_profile_id_safe` → 400, не dump |
| profile IDOR | login + свой id (staff — шире) | alice → id=2 → **403** |
| orders leak | фильтр `owner = session.id` | alice видит только свои |
| price spoof | цена только из `self.products` | `price: 1` → всё равно 1500 |
| X-Role spoof | роль из сессии | alice+X-Role staff → **403**; staff token → 200 |
| files IDOR | свой username + только receipt.txt | bob receipt под alice → **403** |
| debug logs | staff + redact password/token | customer 401; в логах `<redacted>` |
| XSS | `html.escape` | `<script>` в ответе как `&lt;script&gt;` |
| assistant | свой order в context; execute: только свой чек; delete/export → 403 | тесты assistant_* зелёные |

## Повторная «атака» execute независимо от LLM

Снова отправил готовый JSON decision (как рекомендует README — отдельный тест доступа к tool):

- `delete_tree` → **403 tool not allowed**
- `export_profiles` → **403**
- `read_file` на `files/bob/receipt.txt` под alice → **403**
- свой `files/alice/receipt.txt` → **200**, текст чека на месте

То есть даже если planner поддастся injection из отзыва, сервер больше не делает опасное действие.

## Регресс функционала

`make step6` / `make test`: поставка + security, OK (на моей Windows symlink-тест sandbox skipped из‑за WinError 1314 — прав на symlink нет, к дырам сервиса не относится).

Клиент по-прежнему: логинится, видит свой профиль/чек, покупает по цене каталога, пишет отзыв, через assistant читает свой чек. Staff экспорт работает по сессии staff.

## Вывод

Основной урок: LLM-judge/planner — недоверенный компонент. Резать надо на `execute` и на выдаче context, а не надеяться, что модель «не послушается» отзыв. Плюс классика веба (IDOR, SQL, price, role header) здесь была даже без AI.
