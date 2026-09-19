# Unit-проверки

Файл ведёт OpenCode. Обсудите с агентом содержание и проверьте предложенный diff. Все дополнения и исправления поручайте агенту в чате.

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Подтверждение |
|---|---|---|---|---|
| Валидация payload: поле "diff" обязательно ([context.md](context.md)) | Функция create_review должна возвращать HTTP 400, если payload не содержит поля "diff" | `{"wrong_field": "value"}` | HTTP 400 Bad Request, body: `{"error": "Field 'diff' is required"}` | Unit-тест: `test_create_review_missing_diff_field()` с mock review_service |
| Валидация payload: diff должен быть строкой | Функция create_review должна возвращать HTTP 400, если diff не является строкой | `{"diff": 123}` (число вместо строки) | HTTP 400 Bad Request, body: `{"error": "Field 'diff' must be a string"}` | Unit-тест: `test_create_review_invalid_diff_type()` с Pydantic ValidationError |
| Валидация размера diff: лимит 1MB ([product_management.md](product_management.md)) | Функция валидации должна отклонять diff размером >1MB | Строка длиной 1_048_577 байт | ValidationError: `"Diff too large (limit: 1MB)"` | Unit-тест: `test_validate_diff_size_exceeds_limit()` |
| Обработка ошибок LLM: retry при timeout ([adr.md](adr.md)) | Функция review должна повторить запрос к LLM при timeout, затем вернуть ошибку | Mock llm.generate() выбрасывает TimeoutError | После 3 попыток вернуть HTTP 503 Service Unavailable, body: `{"error": "LLM service timeout"}` | Unit-тест: `test_review_llm_timeout_retry()` с mock LLM |
| Формат ответа LLM: ≤3 риска ([prompts.md](prompts.md), Master Prompt v1) | Валидация ответа LLM должна проверять количество рисков | LLM возвращает JSON с 5 рисками | ValidationError: `"Response contains 5 risks, expected ≤3"` | Unit-тест: `test_validate_llm_response_too_many_risks()` |
| Формат риска: обязательные поля file, line, description, check ([prompts.md](prompts.md)) | Валидация риска должна проверять наличие всех обязательных полей | `{"file": "app/api.py", "description": "..."}` (отсутствует line) | ValidationError: `"Risk missing required field: line"` | Unit-тест: `test_validate_risk_missing_field()` с Pydantic model |

## Как использовали AI

- Для чего: Заполнение tests_unit.md — unit-проверки для AI-помощника code review (валидация входа, обработка ошибок LLM, формат ответа)
- Тип промпта: zero-shot (агент OpenCode в режиме Build)
- Строка в [`prompts.md`](prompts.md): (домашняя работа, не отдельный запуск)
- Что проверил студент и какие исправления поручил агенту: Проверить согласованность с adr.md (требования к валидации, обработке ошибок), product_management.md (граничные случаи из Gherkin), prompts.md (формат ответа из Master Prompt v1); убедиться что все проверки изолированные (используют mock для внешних зависимостей)
