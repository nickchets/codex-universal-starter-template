# Онбординг 30 Минут (RU)

## 0) Понять проект (3 мин)
Прочитать:
- `PROJECT_MANIFEST.md`
- `ACTION_PLAN.md`
- `EVIDENCE_LOG.md`
- `DEBUG.md`

## 1) Заполнить стартовые контракты (8 мин)
Обновить:
- `PROJECT_MANIFEST.md` (цель, DoD, ограничения),
- `ACTION_PLAN.md` (текущий `DOING`, `NEXT`, разбиение задачи),
- `docs/DIRECTIVE_REGISTER.md` (первая строка директивы пользователя).

## 2) Bootstrap-проверки (5 мин)
```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label onboarding
```

## 3) Базовая верификация (5 мин)
```bash
./tools/verify_fail_fast.sh
```

## 4) Зафиксировать evidence (4 мин)
Добавить блок в `EVIDENCE_LOG.md`:
- команды,
- PASS/FAIL,
- пути к артефактам.

## 5) Начать реализацию (5 мин)
Взять текущую карточку `DOING`, сделать минимальный безопасный дифф, проверить, перевести состояние доски.
