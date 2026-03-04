### <CARD-ID>

- [ ] Step: `<one atomic action>`
- [ ] Done when: `<observable completion criterion>`
- [ ] Verify/Evidence: `<command or artifact path>`
- [ ] Check-A (contract): `<invariants/policy/contract proof>`
- [ ] Check-B (behavior): `<runtime/live behavior proof>`

- [ ] Step: `<next atomic action>`
- [ ] Done when: `<observable completion criterion>`
- [ ] Verify/Evidence: `<command or artifact path>`
- [ ] Check-A (contract): `<invariants/policy/contract proof>`
- [ ] Check-B (behavior): `<runtime/live behavior proof>`

Rules:
- Use `8-20` steps for medium/high-risk cards.
- Keep each step atomic (one action, one outcome).
- Do not close the card unless both checks are `PASS`.
- If `Check-B` is `INCONCLUSIVE`, add an explicit recheck step with new artifacts.
