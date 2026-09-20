# Журнал экспериментов Практики 2

Файл ведёт OpenCode по вашим запросам. Агент записывает фактические результаты экспериментов и вносит изменения в связанные файлы. Свою оценку сообщайте ему в чате; вручную заполнять шаблон не нужно.

- Выбранный слабый артефакт Практики 1: [`../practice_01/context.md`](../practice_01/context.md)
- Что в нём нужно улучшить: AS IS описывал поведение будущего AI-помощника (TO BE); смешение Context Pack с «текущим процессом»; в «неизвестно» попадал стек, уже видимый в TRAINING_PR.diff; хороший пример риска без точной строки из diff
- Как поймём, что изменение полезно: таблица AS IS совпадает с analysis.md (ручной review, без LLM); Context Pack явно помечен как TO BE; пример риска ссылается на `app/api.py:~10` из TRAINING_PR.diff; неизвестное не содержит опровергнутых фактов

| Техника | Файл эксперимента | Изменённый файл Практики 1 | Конкретное изменение | Проверка | Что отклонили |
|---|---|---|---|---|---|
| Few-shot | [`few_shot/experiment.md`](few_shot/experiment.md) | [`context.md`](../practice_01/context.md) § «Как устроен текущий процесс?» | AS IS = ручной review; помощника в AS IS нет | Сверка с analysis.md AS IS | Старая формулировка «помощник получает diff…» |
| R.C.T.F. | [`rctf/experiment.md`](rctf/experiment.md) | [`context.md`](../practice_01/context.md) заголовки | Секции помечены (AS IS) / (TO BE); вводная к Context Pack | По оглавлению нельзя спутать «сейчас» и помощника | Дублировать flowchart analysis в context |
| Chain of Verification | [`chain_of_verification/experiment.md`](chain_of_verification/experiment.md) | [`context.md`](../practice_01/context.md) системы + неизвестно + факты | LLM убран из AS IS; FastAPI в факты; неизвестное сужено | TRAINING_PR.diff, analysis.md, adr.md | GitHub App ID / бюджет без источника |
| Tree of Thoughts | [`tree_of_thoughts/experiment.md`](tree_of_thoughts/experiment.md) | [`context.md`](../practice_01/context.md) § факты | Приоритет категорий рисков при >3 кандидатах | Согласованность с README ≤3 и кейсом TRAINING_PR | Только-security; «самые длинные» риски |
| RAG | [`rag/experiment.md`](rag/experiment.md) | [`context.md`](../practice_01/context.md) § хороший пример | Пример `app/api.py:~10` + curl; пояснение номеров строк | Пересчёт hunk TRAINING_PR.diff | Строки ~36 и 145 |
| ReAct | [`react/experiment.md`](react/experiment.md) | [`context.md`](../practice_01/context.md) ограничения + футер | Запрет патчей и путаницы номеров; футер → журнал П2 | Чеклист ReAct 5 шагов | Перенос всего ADR в context |
