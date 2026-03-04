# Стартовая Анкета Агента (RU)

Использовать до начала кодинга.

## Что Агент Должен Спросить У Пользователя
1. Какова точная цель текущего цикла (одним предложением)?
2. Какой измеримый Definition of Done для этого цикла?
3. Какие ограничения жесткие (время, безопасность, комплаенс, архитектура)?
4. Что явно вне scope (non-goals)?
5. Какие verify-команды обязательны перед закрытием задачи?
6. Какие внешние источники нужно перепроверить (доки/спеки/актуальные правила)?

## Какие Документы Заполнить До Старта Работы
1. `PROJECT_MANIFEST.md`
   - цель
   - DoD
   - ограничения
   - non-goals
2. `ACTION_PLAN.md`
   - ровно одна карточка `DOING`
   - максимум три карточки `NEXT`
   - task breakdown для текущего `DOING`
3. `docs/DIRECTIVE_REGISTER.md`
   - директива пользователя verbatim
   - intent (`EXEC_NOW` или `WORKFLOW_IDEA`)
   - planned integration
   - verify hook
4. `EVIDENCE_LOG.md`
   - первый bootstrap evidence-блок

## Обязательные Стартовые Команды
```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label startup
python3 tools/dev_harness_server.py update-plan-sync --summary "startup snapshot" --status IN_PROGRESS --label startup
./tools/verify_fail_fast.sh
```
