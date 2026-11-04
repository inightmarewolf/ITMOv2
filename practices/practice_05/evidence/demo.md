# Демо сквозного сценария

Подписчики живут **в памяти процесса**, поэтому цепочку команд гоняем одним процессом:

```bash
cd practices/practice_04/lab
make test
python scripts/demo_flow.py
```

`demo_flow.py` вызывает `cli.main([...])` несколько раз подряд: subscribe → list → unsubscribe → list → unknown name.

Сырой вывод: `make-test.txt`, `cli-demo.txt`.

Проверяемые границы:
- happy path отписки
- `unknown name` → exit 1
- старые сценарии A/B зелёные в unittest
