# Протокол Синхронизации Контекста (RU)

Цель:
- гарантировать, что каждая директива пользователя зафиксирована, привязана к плану и проверена.

## Канонический Порядок Загрузки
1. `PROJECT_MANIFEST.md`
2. `docs/ADR/README.md`
3. `ACTION_PLAN.md`
4. `EVIDENCE_LOG.md`
5. `DEBUG.md`
6. `docs/CONTEXT_SYNC_PROTOCOL.ru.md`
7. `docs/DIRECTIVE_REGISTER.md`

## Обязательная Транзакция (На Каждую Директиву)
1. Классифицировать intent:
   - `EXEC_NOW`
   - `WORKFLOW_IDEA`
2. Зафиксировать директиву verbatim в реестре.
3. Привязать директиву к карточке доски в `ACTION_PLAN.md`.
4. Обновить контракты в `PROJECT_MANIFEST.md`, если меняется поведение/приемка.
5. Прогнать governance gate:
   - `python3 tools/dev_harness_server.py workflow-context-gate --label <name>`
6. Добавить evidence-блок с командами и артефактами в `EVIDENCE_LOG.md`.

## Правила Неоднозначности
- Нельзя закрывать `DOING->DONE` без evidence.
- Нельзя терять директиву без записи в реестре.
- Нельзя работать с невалидной доской (`DOING != 1` или `NEXT > 3`).
