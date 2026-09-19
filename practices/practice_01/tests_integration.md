# Integration-проверки

Файл ведёт OpenCode. Обсудите с агентом содержание и проверьте предложенный diff. Все дополнения и исправления поручайте агенту в чате.

| Связь компонентов | Что может сломаться | Как воспроизводим | Ожидаемый результат | Подтверждение |
|---|---|---|---|---|
| Review API → LLM Service (VseLLM API) ([adr.md](adr.md)) | LLM сервис недоступен (HTTP 503, timeout, network error) | Запустить Review API с mock LLM endpoint, который возвращает HTTP 503 или таймаут после 5 секунд | API возвращает HTTP 503 Service Unavailable, body: `{"error": "LLM service unavailable"}`, после 3 retry-попыток | Integration-тест: `test_review_llm_service_unavailable()` с testcontainers или mock HTTP server |
| Review API → LLM Service: передача master prompt + diff | Master prompt не передаётся корректно в LLM, LLM возвращает некорректный ответ | Запустить Review API с реальным LLM API (staging), передать TRAINING_PR.diff | LLM возвращает отчёт с ≤3 рисками, каждый содержит file, line, description, check. API возвращает HTTP 200, body содержит отчёт в формате markdown | Integration-тест: `test_review_with_real_llm_training_diff()` (используем staging LLM API key) |
| Review API → GitHub/GitLab webhook | Webhook signature validation: некорректная подпись HMAC | Отправить POST /api/reviews с заголовком X-Hub-Signature-256, но с неверной подписью | API возвращает HTTP 401 Unauthorized, body: `{"error": "Invalid webhook signature"}` | Integration-тест: `test_webhook_invalid_signature()` |
| Review API → GitHub API: создание комментария в PR | GitHub API возвращает HTTP 403 (нет прав на запись комментариев) | Mock GitHub API endpoint POST /repos/{owner}/{repo}/issues/{pr}/comments, возвращающий HTTP 403 | API логирует ошибку "GitHub API: permission denied", но не падает. Возвращает HTTP 200 с предупреждением: `{"warning": "Failed to post comment to PR"}` | Integration-тест: `test_post_comment_github_api_forbidden()` с mock GitHub API |
| Полный цикл: Webhook → Review API → LLM → GitHub comment | Любой компонент может сломаться; проверяем end-to-end взаимодействие | Настроить тестовый GitHub репозиторий с webhook, открыть PR с TRAINING_PR.diff, дождаться комментария от бота | В PR появляется комментарий от GitHub App с отчётом (≤3 риска, markdown). Комментарий содержит риск KeyError на payload["diff"] с app/api.py:~10 | E2E-тест (не integration): перенести в tests_e2e.md |

## Как использовали AI

- Для чего: Заполнение tests_integration.md — integration-проверки для AI-помощника code review (связь Review API ↔ LLM, Review API ↔ GitHub/GitLab)
- Тип промпта: zero-shot (агент OpenCode в режиме Build)
- Строка в [`prompts.md`](prompts.md): (домашняя работа, не отдельный запуск)
- Что проверил студент и какие исправления поручил агенту: Проверить согласованность с adr.md (архитектурная схема, компоненты), product_management.md (сценарии ошибок из Gherkin); убедиться что проверки действительно integration (используют несколько компонентов, а не mock всё); отделить E2E-проверки (полный цикл через GitHub) в tests_e2e.md
