# Skill Authoring Guidelines

Purpose:
- keep `SKILL.md` files precise, selectable, and execution-ready.

## Recommended Structure

1. Front matter
   - `name`
   - one-sentence `description` (what it is + when to use)
   - optional metadata (`short-description`, tags)
2. Core mission
3. Trigger conditions
4. Boundaries / non-goals
5. Principles
6. Required outputs/artifacts
7. Canonical workflow
8. Acceptance criteria
9. Anti-patterns

## Quality Rules

- Keep the description scope explicit so skill selection is reliable.
- Prefer actionable checklists over abstract advice.
- Make each phase verifiable with commands or artifacts.
- Use deterministic exit criteria.
- Avoid hidden assumptions between phases.

## Progressive Disclosure

- Keep core flow in `SKILL.md`.
- Move large templates/examples into `references/` or workflow files when needed.
- Link scripts/assets instead of duplicating large blocks.

## Source Notes

The structure above follows guidance from:
- OpenAI Codex skills docs (clear scope/description, concise skills, progressive disclosure)
- OpenAI Apps SDK skills planning docs (clear invocation scope and maintainability)
- AgentSkills standard format (structured sections and execution clarity)
