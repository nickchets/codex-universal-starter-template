# Стартовый Промпт Для Агента (RU)

Используйте это как первое сообщение Codex в новом проекте:

```text
Работай в автономном режиме выполнения.
Перед реализацией:
1) Запусти bootstrap и context gate.
2) Синхронизируй снимок активного плана через update-plan-sync.
3) Задай мне стартовые вопросы из docs/AGENT_STARTUP_QUESTIONNAIRE.ru.md.
4) Заполни/обнови PROJECT_MANIFEST.md, ACTION_PLAN.md, docs/DIRECTIVE_REGISTER.md.
5) Подтверди инварианты доски (DOING==1, NEXT<=3).
Дальше делай минимальные безопасные диффы, верифицируй и фиксируй evidence в EVIDENCE_LOG.md.
```
