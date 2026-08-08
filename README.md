# Cross-Domain Trace Set (CDTS)

[![CDTS checks](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml/badge.svg)](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml)

**Artifact version:** `0.2`
**Record profile:** `0.1`
**Canonical status:** `canonical_public`
**License:** MIT

CDTS is a portable coordination-layer trace for correlating addressable records owned by independent specifications.

> Import the trace, not the conclusion.

It records a bounded correlation scope, exact source revisions, qualified external references, CDTS-owned linkage assertions, typed absence, disclosed conflict, unresolved questions, provenance, and amendment history.

CDTS does not validate an external record, import a domain verdict, establish event identity, prove causality, evaluate expected-record completeness, authenticate external producers, or evaluate world truth.

## Five normative surfaces

| Surface | Owns |
|---|---|
| `spec/01_CDTS_CORE.md` | trace semantics, ownership boundaries, and admissibility requirements |
| `spec/02_RELATIONSHIP_VOCABULARY.md` | CDTS relationship, status, and basis meanings |
| `spec/03_SOURCE_REVISION_POLICY.md` | owner, role, pin, and compatibility-set rules |
| `spec/04_CONFORMANCE.md` | pipeline, statuses, exit codes, and implementation obligations |
| `schema/cdts-record.schema.json` | structural representation of record profile `0.1` |

```text
normative_surface_count = 5
reference validator      = non-normative implementation
compatibility receipt    = exact reviewed values, not a sixth specification
```

## Start

```bash
python validator/cdts_validate.py examples/mpaa-bec-execution.json
python -m unittest discover -v
python -m review.test_artifact_canon
```

An `ADMISSIBLE` result establishes machine-checkable CDTS structural, local-reference, source-pin, and boundary conformance. It does not establish external completeness, authenticity, identity, causality, native-record validity, or truth. Every result reports `world_truth` as `NOT_EVALUATED`.

## Current compatibility set

The active fixed revisions are recorded in `references/PINNED_SPEC_REVISIONS.md`:

```text
BEC             62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261
MPAA            0d1aaf35cc4826622f3312fdd2a1c2d40890b965
PCA             a669f023198615ad929f42df84f19380b57ca5ea
Review Protocol b4205ffd91a6316ab40243cbf8161a1c512cae1f
ARB             bcf9f628ee1d7c2075673b00f660674680bb6f62
```

MPAA, BEC, and PCA remain authoritative only for their own records and conclusions. Review Protocol supplies source-selection discipline only. ARB is analytical mapping only and cannot be a normative owner.

## External-evaluation trace profile

`examples/external-evaluation-run.json` correlates one synthetic MPAA Runtime Report reference with one synthetic BEC acceptance-run reference around an exact donor artifact SHA-256.

The donor digest is a correlation key, not an authenticity, completeness, privacy, safety, provenance, or redaction verdict. The example remains `ADMISSIBLE_WITH_UNRESOLVED` because several claims require evidence outside CDTS. It records typed PCA absence without treating absence as process-continuation failure.

## Canonical surfaces

- `CANON.md` - authority model, exact-source rule, gates, and limits;
- `ARTIFACT.json` - machine identity, surface matrix, checks, boundaries, and relations;
- `RELATIONS.md` - five fixed neighboring relations;
- `PROVENANCE.md` - origin, version separation, history, license, and participation boundary;
- `spec/` - normative human-readable corpus plus the non-normative quick guide;
- `schema/` - normative record representation;
- `references/PINNED_SPEC_REVISIONS.md` - active compatibility receipt;
- `validator/` - non-normative reference implementation;
- `conformance/` - examples and resistance evidence;
- `review/` - historical review and executable artifact checks.

## Reading order

1. `CANON.md`
2. `ARTIFACT.json`
3. `spec/00_CDTS_IN_60_SECONDS.md`
4. `spec/01_CDTS_CORE.md`
5. `spec/02_RELATIONSHIP_VOCABULARY.md`
6. `spec/03_SOURCE_REVISION_POLICY.md`
7. `spec/04_CONFORMANCE.md`
8. `schema/cdts-record.schema.json`
9. `RELATIONS.md`
10. `PROVENANCE.md`

No multi-implementation conformance claim is made.
