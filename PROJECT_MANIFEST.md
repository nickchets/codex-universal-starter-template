# PROJECT_MANIFEST

Use this file as the project-level contract.

## 1. Context
- Project name: `<fill>`
- Problem statement: `<fill>`
- Primary users: `<fill>`
- Scope boundary: `<fill>`

## 2. Objective + DoD
- Objective: `<fill>`
- Definition of Done (measurable):
  - `<fill>`
  - `<fill>`
  - `<fill>`

## 3. Constraints
- Technical constraints:
  - `<fill>`
- Compliance/security constraints:
  - `<fill>`
- Delivery constraints:
  - `<fill>`

## 4. Non-Goals
- `<fill>`
- `<fill>`

## 5. Architecture Contract
- Core components:
  - `<fill>`
- Critical interfaces:
  - `<fill>`
- Failure handling policy:
  - `<fill>`

## 6. Verification Contract
- Minimum checks:
  - `./tools/verify_fail_fast.sh`
- Integration/e2e checks:
  - `<fill>`
- Acceptance artifacts expected:
  - `<fill>`

## 7. Governance Invariants
- Board states: `NEXT`, `DOING`, `BLOCKED`, `DONE`.
- Allowed transitions only:
  - `NEXT->DOING`
  - `DOING->BLOCKED`
  - `BLOCKED->DOING`
  - `DOING->DONE`
- Board invariants:
  - `DOING == 1`
  - `NEXT <= 3`
