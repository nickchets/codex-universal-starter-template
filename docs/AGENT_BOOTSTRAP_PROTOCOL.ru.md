# Протокол Bootstrap Агента (RU)

Запускать, если:
- новый чат,
- контекст сомнительный,
- агент не может уверенно назвать текущую карточку `DOING`.

## Обязательная Цепочка
1. Выполнить:
   - `python3 tools/agent_bootstrap.py`
   - `python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap`
   - `python3 tools/dev_harness_server.py update-plan-sync --summary "bootstrap snapshot" --status IN_PROGRESS --label bootstrap`
2. Загрузить контекст строго по порядку:
   - `PROJECT_MANIFEST.md`
   - `docs/ADR/README.md`
   - `ACTION_PLAN.md`
   - `EVIDENCE_LOG.md`
   - `DEBUG.md`
   - `docs/CONTEXT_SYNC_PROTOCOL.ru.md`
3. Проверить инварианты доски:
   - `DOING == 1`
   - `NEXT <= 3`
4. Начинать работу только после PASS.

## Условие Остановки
Если bootstrap-проверки не пройдены, сначала чинить целостность docs/board, и только потом идти в feature-работу.
