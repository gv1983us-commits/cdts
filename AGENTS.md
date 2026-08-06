# CDTS Contributor Instructions

Read in this order:

1. `CANON.md`
2. `ARTIFACT.json`
3. the five normative surfaces
4. `RELATIONS.md`
5. `PROVENANCE.md`
6. the compatibility receipt
7. validator, examples, fixtures, and review tests

Preserve the five-surface domain-ownership matrix. Do not make the validator, fixtures, examples, compatibility receipt, publication checker, or House representation a sixth normative surface.

Preserve external ownership boundaries: MPAA, BEC, and PCA own their records and conclusions; Review Protocol owns review discipline; ARB is analytical only; CDTS owns trace structure, its namespaced linkage assertions, and CDTS admissibility.

Use exact fixed revisions. Never rewrite historical review logs as though they inspected later commits. A new compatibility set requires an explicit review and a new artifact revision.

Use strict RED-GREEN-REFACTOR for validator changes, standard-library Python in the reference implementation, strict JSON parsing, schema/validator parity tests, and fail-closed handling of unsupported normative schema assertions.

Public files must contain neutral infrastructure material and no credentials, private share links, local paths, or secret-bearing data.

Publication requires explicit human authorization. The current canonization is authorized by the repository authority through the active project session; future automation must not infer standing publication authority from this event.
