# Подтверждение применения среды в OpenCode (VseLLM)

Команда:

```bash
opencode run --auto --format json --dir . -m vsellm/openai/gpt-5 \
  "Прочитай AGENTS.md. Загрузи skill notify-tests. Вызови MCP subscribe_name ..."
```

Сырой лог: `evidence/opencode_run.jsonl`

## Что реально вызвал агент

1. **read** `AGENTS.md` — увидел фичи A/B и правила.
2. **skill** `notify-tests` — загрузил процедуру + `writing-good-tests.md`.
3. **MCP** `notify_subscribe_name`:
   - `name=Ann` → `{"ok": true, "result": {"subscribed": true, "name": "Ann"}, ...}`
   - `name="   "` → `{"ok": false, "error": "empty name"}`

Первый прогон: код не менялся.  
Второй прогон (`opencode_hook_run.jsonl`): агент сделал `apply_patch` → **сработал hook** и вернул `OK` по тестам. См. `evidence/hook_runner.md`.
