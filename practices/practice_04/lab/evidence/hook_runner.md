# Hook + runner — подтверждение через OpenCode / VseLLM

- Plugin: `.opencode/plugins/check-after-edit.js`
- Событие: `tool.execute.after` на `apply_patch` / `edit` / `write`
- Runner: `python scripts/check.py`

## Живой прогон

`opencode run -m vsellm/openai/gpt-5` попросил добавить комментарий `# hook-demo` в `service.py`.

В ответе tool `apply_patch` агент получил блок hook:

```text
--- hook check-after-edit: python scripts/check.py ---
test_duplicate ... ok
test_empty ... ok
test_list ... ok
test_subscribe ... ok
Ran 4 tests in 0.000s
OK
exit: 0
--- end hook ---
```

Сырой лог: `evidence/opencode_hook_run.jsonl`
