# CDTS Conformance

## Pipeline

1. Strict UTF-8 JSON parsing rejects syntax errors, duplicate keys, NaN, and infinities.
2. Structural schema validation rejects missing fields, additional fields, malformed timestamps/digests, and unknown tokens.
3. Local identity and reference checks reject duplicate CDTS IDs, dangling references, and self-links.
4. Fixed-source checks enforce owner, revision, role, and record-reference parity.
5. Boundary checks reject dedicated imported-conclusion fields and a purported current PCA Linkage Record. The validator does not semantically classify free-text values.
6. Temporal checks validate scope/provenance order and temporal link assertions.
7. Conflict, unresolved, and amendment checks enforce internal reference completeness, chain continuity, and external-policy boundaries.
8. The validator derives admissibility.

## Results

- `ADMISSIBLE` (exit 0)
- `INVALID` (exit 1)
- parser/tool/schema failure (exit 2)
- `ADMISSIBLE_WITH_CONFLICTS` (exit 3)
- `ADMISSIBLE_WITH_UNRESOLVED` (exit 4)
- both qualifications (exit 5)

Qualified admissibility is not failure: explicit conflict and uncertainty are valid trace states. Every result reports world truth as `NOT_EVALUATED`.

A conforming implementation MUST fail closed on unsupported normative schema assertions and MUST pass the fixture corpus. v0.1 has one reference implementation and makes no multi-implementation claim.
