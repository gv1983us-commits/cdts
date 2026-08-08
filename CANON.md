# Cross-Domain Trace Set - Canon

**Artifact:** Cross-Domain Trace Set (CDTS)
**Corpus identity:** `claude.cdts`
**Repository:** `gv1983us-commits/cdts`
**Artifact version:** `0.2`
**Record profile:** `0.1`
**Canonical status:** `canonical_public`
**License:** MIT

This document declares how CDTS is read, cited, checked, and changed as one public technical artifact.

Canonicalization preserves the existing v0.1 trace profile. It does not upgrade an admissible trace into proof of an external event, external conclusion, identity, causality, authenticity, completeness, or world truth.

## 1. Five-surface authority rule

CDTS has five normative surfaces with separate domains:

| Surface | Path | Normative domain |
|---|---|---|
| CDTS Core | `spec/01_CDTS_CORE.md` | trace semantics, ownership boundaries, and admissibility requirements |
| Relationship Vocabulary | `spec/02_RELATIONSHIP_VOCABULARY.md` | meanings of CDTS-namespaced relationship, status, and basis tokens |
| Source Revision Policy | `spec/03_SOURCE_REVISION_POLICY.md` | owner, role, pin, and compatibility-set rules |
| Conformance | `spec/04_CONFORMANCE.md` | validation pipeline, result statuses, exit codes, and implementation obligations |
| Record Schema | `schema/cdts-record.schema.json` | structural representation of record profile `0.1` |

```text
normative_surface_count = 5
```

No sixth normative surface is created by the validator, examples, fixtures, compatibility receipt, publication tests, or House representation.

## 2. Domain ownership

When two surfaces overlap, each owns only its declared domain:

```text
trace meaning and admissibility rules -> Core
CDTS token meaning                   -> Relationship Vocabulary
pin and role discipline              -> Source Revision Policy
validation result semantics          -> Conformance
JSON object shape                     -> Record Schema
execution of checks                   -> reference validator
```

The reference validator may operationalize several surfaces. It cannot amend them by implementation behavior.

## 3. Compatibility receipt boundary

`references/PINNED_SPEC_REVISIONS.md` records the exact five-source compatibility set reviewed for this artifact revision.

It is canonical evidence of the reviewed source state, but it is not a sixth abstract specification. Source Revision Policy owns the rule that exact pins and roles are required. The receipt supplies the accepted values for this candidate.

A future pin update requires an explicit compatibility review and a new CDTS revision. It is not an editorial replacement of `latest` values.

## 4. External ownership boundary

CDTS owns:

- the bounded trace scope;
- qualified external references;
- typed absences;
- CDTS-namespaced linkage assertions;
- disclosed conflicts;
- explicit unresolved questions;
- local provenance and amendment structure;
- CDTS admissibility.

CDTS does not own the content, validity, terminology, or conclusion of MPAA, BEC, or PCA records. Review Protocol supplies review discipline. ARB is analytical context only.

```text
import the trace != import the conclusion
correlation != event identity
sequence != causality
ADMISSIBLE != external truth
```

## 5. Reference implementation boundary

`validator/cdts_validate.py` is a fail-closed reference implementation.

It is not:

- a sixth normative surface;
- a native MPAA, BEC, or PCA validator;
- an authenticity oracle;
- a completeness evaluator;
- an identity or causality evaluator;
- a world-truth evaluator.

Its standard-library schema interpreter deliberately supports a bounded audited subset. Unsupported normative schema assertions produce tool failure rather than silent acceptance.

## 6. Exact-source rule

A reproducible claim about CDTS must cite an exact commit or immutable release identifier. `main` alone is a moving development line.

Neighbor relations are independently fixed reviews. Reciprocal relations do not require an impossible mutual-SHA fixpoint:

```text
an older artifact may pin an earlier CDTS revision
this CDTS revision may pin that artifact's later accepted revision
both statements remain exact historical reviews
neither statement means latest
```

## 7. Canonical verification

From the repository root:

```bash
python -m unittest discover -v
python -m json.tool ARTIFACT.json >/dev/null
python validator/cdts_validate.py examples/mpaa-bec-execution.json
python -m review.test_artifact_canon
```

GitHub Actions runs the complete suite on Python 3.10, 3.11, 3.12, and 3.13. The external `jsonschema` package is a test oracle only; the reference validator remains standard-library-only.

Passing establishes internal artifact and trace-profile conformance at the tested revision. It does not establish the truth of referenced records or external-world claims.

## 8. Acceptance gates

A revision is admissible to the canonical line only when:

1. all five normative surfaces are present and domain-separated;
2. the validator remains non-normative and fail-closed;
3. the exact compatibility set is documented and machine-enforced;
4. every external conclusion remains unimported;
5. causal vocabulary remains absent from profile v0.1;
6. typed absence, conflicts, unresolved questions, and amendments remain explicit;
7. schema and validator parity tests pass;
8. all canonical examples and resistance fixtures produce their expected results;
9. MIT remains tied to the published `LICENSE`;
10. all supported CI versions pass.

## 9. Canon limits

This canon does not establish:

- event identity;
- causality;
- external record validity or authenticity;
- expected-record completeness;
- external producer identity or independence;
- predecessor digest correspondence;
- neighboring conformance;
- multi-implementation conformance;
- identity, memory, consciousness, or subjectivity;
- world truth.

> CDTS closes the six-artifact corpus by carrying exact relations without taking ownership of what the related domains alone can decide.
