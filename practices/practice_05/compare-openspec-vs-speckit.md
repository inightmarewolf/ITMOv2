# Сравнение: OpenSpec vs Spec Kit (на одной фиче)

Фича одна: **unsubscribe + CLI** в Notify Mini.

## Что делал в каждом

| | OpenSpec | Spec Kit (артефакты) |
|---|---|---|
| Старт | `openspec init` + change `unsubscribe-cli` | `constitution` + `spec` + `plan` + `tasks` |
| Артефакты | proposal → delta specs → design → tasks | плоские md без delta/archive |
| Проверка структуры | `openspec validate --strict` | глазами / по чеклисту |
| После приёмки | `openspec archive` → main specs | ручное «спека актуальна» |
| Где лежит | `practice_04/lab/openspec/` | `practice_05/other-sdd/spec-kit/` |

## Чем OpenSpec удобнее на brownfield

- Есть явный change и archive: видно историю изменения требований.
- `validate` ловит кривой формат сценариев (у меня сначала чуть не забыл `#### Scenario`).
- Skills/команды завязаны на coding client — проще не спрыгнуть сразу в код.

## Чем Spec Kit проще / где overhead

- Меньше церемонии: четыре файла и поехал — на крошечном Notify Mini этого хватает.
- Constitution жёстче задаёт «закон проекта», OpenSpec у меня скорее rules в `config.yaml`.
- На такой мелкой фиче Spec Kit-документы почти дублируют dual-spec; ощущение waterfall из лекции здесь реально ловится.

## Вывод для сдачи

Код оставил от **OpenSpec** (с archive и main specs). Spec Kit прогнал как второй каркас документации на ту же фичу и сравнил процесс. Для задачи размера «одна функция + CLI» OpenSpec тяжелее стартом, но archive/validate полезнее, если спеки живут дольше одной домашки.
