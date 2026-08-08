# CDTS Conformance - Profile v0.1

**Status:** normative
**Artifact version:** `0.2`
**Normative domain:** validation pipeline, result statuses, exit codes, and conforming-implementation obligations

## Pipeline

1. Strict UTF-8 JSON parsing rejects syntax errors, duplicate keys, NaN, and infinities.
2. Structural schema validation rejects missing fields, additional fields, malformed timestamps or digests, and unknown tokens.
3. Local identity and reference checks reject duplicate CDTS IDs, dangling references, and self-links.
4. Fixed-source checks enforce owner, revision, role, and record-reference parity.
5. Boundary checks reject dedicated imported-conclusion fields and a purported current PCA Linkage Record. The validator does not semantically classify free-text values.
6. Temporal checks validate scope/provenance order and temporal linkage assertions.
7. Conflict, unresolved, and amendment checks enforce internal reference completeness, chain continuity, and external-policy boundaries.
8. The implementation derives admissibility; the producer cannot self-award it inside the trace.

## Results and exit codes

| Result | Exit code |
|---|---:|
| `ADMISSIBLE` | 0 |
| `INVALID` | 1 |
| parser, schema, or tool failure | 2 |
| `ADMISSIBLE_WITH_CONFLICTS` | 3 |
| `ADMISSIBLE_WITH_UNRESOLVED` | 4 |
| conflicts and unresolved qualifications | 5 |

Qualified admissibility is not failure: explicit conflict and uncertainty are valid trace states.

Every result reports `world_truth: NOT_EVALUATED`.

## Implementation conformance

A conforming implementation MUST:

- implement all applicable Core, Vocabulary, Source Revision Policy, Schema, and Conformance requirements;
- fail closed on unsupported normative schema assertions;
- reject producer-authored validation surfaces;
- pass the canonical fixture and resistance corpus;
- preserve result and exit-code semantics;
- avoid importing neighboring conclusions.

Profile v0.1 has one reference implementation and makes no multi-implementation conformance claim.
