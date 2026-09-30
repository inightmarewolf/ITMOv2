# E2E-проверки

Файл ведёт OpenCode. Обсудите с агентом содержание и проверьте предложенный diff. Все дополнения и исправления поручайте агенту в чате.

| Сценарий пользователя | Предусловия | Действие | Наблюдаемый результат | Подтверждение |
|---|---|---|---|---|
| Позитивный: ревьюер получает отчёт по реальному PR | Staging: Review API + LLM + GitHub App с правом писать комментарии; webhook на `pull_request` opened/synchronize; в репозитории есть ветка с изменениями из [TRAINING_PR.diff](TRAINING_PR.diff) | Открыть PR (или запушить коммит в PR). Дождаться автоматического комментария бота | В PR появляется markdown-комментарий от GitHub App: ≤3 риска; есть риск KeyError на `payload["diff"]` с файлом `app/api.py` (~строка 10) и воспроизводимой проверкой `curl -X POST ... -d '{}'`; помощник не approve/merge и не меняет код | E2E: открыть PR в тестовом репо, сохранить screenshot/ссылку на комментарий; сверить с ожидаемым форматом из [product_management.md](product_management.md) |
| Негативный: LLM недоступен во время ревью | Тот же staging; LLM stub/mock возвращает HTTP 503 или timeout | Открыть PR с валидным diff | В PR нет «успешного» отчёта с рисками; либо комментарий/статус «LLM unavailable / retry later», либо CI job failed с понятной ошибкой; ревьюер может продолжить ревью вручную; API не падает без логов | E2E: отключить/заглушить LLM, открыть PR, проверить отсутствие ложного «чистого» отчёта и наличие ошибки в логах Review API |
| Граничный: пустой или только formatting-diff | PR без смысловых изменений (пустой diff или только whitespace/formatting) | Открыть такой PR | Комментарий помощника: «No changes found» / «No critical issues found» или 0 рисков; нет выдуманных проблем; ревьюер не получает ложных KeyError-рисков | E2E: PR с пустым/formatting-only diff; проверить текст комментария |

## Как использовали AI

- Для чего: ДЗ Практики 1 — заполнение E2E-сценариев полного цикла webhook → Review API → LLM → комментарий в PR
- Тип промпта: master prompt (агент OpenCode в режиме Build)
- Строка в [`prompts.md`](prompts.md): P1-03
- Что проверил студент и какие исправления поручил агенту: согласовать с [product_management.md](product_management.md) (позитив/негатив/граница), [tests_integration.md](tests_integration.md) (полный цикл вынесен сюда), [TRAINING_PR.diff](TRAINING_PR.diff)
