# Универсальный Starter Template для Codex

Шаблон репозитория для запуска новых проектов с Codex по детерминированному циклу:
`intake -> plan -> implement -> verify -> evidence`.

Шаблон извлечен из боевой dev-обвязки и обезличен для универсального применения.

## Что Внутри

- Контракты управления:
  - `PROJECT_MANIFEST.md` (требования и критерии приемки)
  - `ACTION_PLAN.md` (план и доска задач)
  - `EVIDENCE_LOG.md` (факты проверки и артефакты)
  - `DEBUG.md` (только проверенные runbook-команды)
- Машина состояний доски:
  - состояния: `NEXT`, `DOING`, `BLOCKED`, `DONE`
  - разрешенные переходы:
    - `NEXT->DOING`
    - `DOING->BLOCKED`
    - `BLOCKED->DOING`
    - `DOING->DONE`
  - инварианты:
    - `DOING == 1`
    - `NEXT <= 3`
- Протокол сохранения контекста:
  - порядок bootstrap-загрузки
  - реестр директив пользователя
  - цикл обновления плана (`sync/freshness/trace`)
  - workflow context gate
- Легкие инструменты:
  - `tools/agent_bootstrap.py`
  - `tools/dev_harness_server.py` (governance gate в CLI)
  - `tools/agent_metrics.py`
  - `tools/verify_fail_fast.sh`

## Быстрый Старт (5-10 мин)

1. Клонируйте шаблон и зайдите в репо.
2. Сначала заполните:
   - `PROJECT_MANIFEST.md`
   - `ACTION_PLAN.md`
   - `docs/DIRECTIVE_REGISTER.md`
3. Выполните bootstrap и context gate:

```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap
python3 tools/dev_harness_server.py update-plan-sync --summary "bootstrap snapshot" --status IN_PROGRESS --label bootstrap
```

4. Запустите базовую проверку:

```bash
./tools/verify_fail_fast.sh
```

## Стартовые Вопросы Агенту

Смотрите:
- `docs/AGENT_STARTUP_QUESTIONNAIRE.en.md`
- `docs/AGENT_STARTUP_QUESTIONNAIRE.ru.md`
- `docs/AGENT_START_PROMPT.en.md`
- `docs/AGENT_START_PROMPT.ru.md`

Там описано:
- что агент должен спросить у пользователя до кодинга,
- какие документы обязательно заполнить до начала работы.

## Карта Документации

- На английском:
  - `docs/AGENT_BOOTSTRAP_PROTOCOL.en.md`
  - `docs/CONTEXT_SYNC_PROTOCOL.en.md`
  - `docs/NETWORK_SEARCH_PROTOCOL.en.md`
  - `docs/ONBOARDING_30_MIN.en.md`
- На русском:
  - `docs/AGENT_BOOTSTRAP_PROTOCOL.ru.md`
  - `docs/CONTEXT_SYNC_PROTOCOL.ru.md`
  - `docs/NETWORK_SEARCH_PROTOCOL.ru.md`
  - `docs/ONBOARDING_30_MIN.ru.md`
- Профиль настройки проекта:
  - `docs/PROJECT_PROFILE.md`
- Благодарности:
  - `docs/ACKNOWLEDGEMENTS.md`

## Лицензия

Репозиторий использует лицензию MIT.
См. файл `LICENSE`.

## Сообщество

- Руководство по вкладу: `CONTRIBUTING.md`
- Руководство по вкладу (RU): `CONTRIBUTING.ru.md`
- Кодекс поведения: `CODE_OF_CONDUCT.md`
- GitHub-шаблоны:
  - `.github/PULL_REQUEST_TEMPLATE.md`
  - `.github/ISSUE_TEMPLATE/*`
- CI workflow:
  - `.github/workflows/ci.yml`

## Публикация в приватный GitHub-репозиторий

```bash
git init
git add .
git commit -m "chore: initialize codex universal starter template"

# Требуется авторизованный GitHub CLI (gh auth status)
gh repo create <your-private-repo-name> --private --source . --remote origin --push
```

## Важно

- Это governance/template-репозиторий, а не доменная бизнес-реализация.
- Держите процессную документацию короткой, явной и подтвержденной evidence.
