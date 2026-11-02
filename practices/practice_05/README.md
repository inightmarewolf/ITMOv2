# Практика / ДЗ 5 — Spec-driven на Notify Mini

Код и OpenSpec живут в [`../practice_04/lab`](../practice_04/lab) (brownfield с практики 4).  
Здесь — артефакты сдачи ДЗ5: dual-spec, Spec Kit, сравнение, демо, рефлексия.

## Фича

**Unsubscribe + CLI** для Notify Mini:
- логика: `unsubscribe(name)` в `service.py`
- UI: текстовый `cli.py` (`subscribe` / `list` / `unsubscribe` / `help`)

## Что где лежит

| Путь | Содержание | Баллы |
|---|---|---:|
| `dual-spec/` | UI и логика до/после + общий контракт | 2 |
| `other-sdd/spec-kit/` + `compare-openspec-vs-speckit.md` | второй SDD и сравнение с OpenSpec | 2 |
| `../practice_04/lab/` (код, тесты, `openspec/`) | реализация + сквозные проверки | 5 |
| `reflection.md` | что согласовали и чему научились | 1 |
| `evidence/` | вывод `make test` и ручное демо CLI | — |
| `practice-part2-config.md` | правило OpenSpec design + фрагмент до/после | занятие |

## Быстрая проверка

```bash
cd ../practice_04/lab
make test
python cli.py subscribe Ann
python cli.py list
python cli.py unsubscribe Ann
```
