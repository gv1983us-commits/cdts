# Cross-Domain Trace Set (CDTS)

[![CDTS checks](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml/badge.svg)](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml)

**Status:** v0.1-draft, exploratory public draft.

CDTS is a portable correlation trace for addressable records owned by independent specifications. It records a bounded correlation scope, fixed source revisions, qualified external references, CDTS-owned linkage assertions, typed absence, disclosed conflict, unresolved questions, provenance, and amendment history.

> Import the trace, not the conclusion.

CDTS does not validate an external record, import a domain verdict, establish event identity, prove causality, or evaluate world truth. MPAA, BEC, and PCA remain authoritative only for their own records and conclusions. ARB-04 is pinned only as an analytical map. Review Protocol supplies source-selection discipline only.

## Start

```bash
python validator/cdts_validate.py examples/mpaa-bec-execution.json
python -m unittest discover -v
```

The validator uses only the Python standard library. An `ADMISSIBLE` result establishes machine-checkable structural conformance, local reference integrity, fixed-source consistency, and CDTS boundary checks. It does not semantically classify free text or establish external completeness, identity, authenticity, or truth. It reports `world_truth` as `NOT_EVALUATED`.

GitHub Actions compiles the validator and publication checker, runs the complete regression and Draft 2020-12 parity suites, repeats the publication checks explicitly, and validates the canonical examples on Python 3.10, 3.11, 3.12, and 3.13. The `jsonschema` package is used only as a CI test oracle; the reference validator remains standard-library-only.

## External-evaluation trace profile

[`examples/external-evaluation-run.json`](examples/external-evaluation-run.json)
correlates one synthetic MPAA Runtime Report reference with one synthetic BEC
acceptance-run record around an exact donor artifact SHA-256. The donor digest is
only a correlation key. It is not an authenticity, completeness, safety, or
redaction verdict.

The example deliberately remains `ADMISSIBLE_WITH_UNRESOLVED` because donor
redaction, evaluator provenance, and external-world effects require evidence
outside CDTS. It also records a typed PCA absence because the black-box run makes
no process-continuation claim.

The trace demonstrates that:

- MPAA and BEC conclusions remain external and are not imported;
- a shared donor receipt supports correlation, not event identity or causality;
- BEC acceptance evidence does not certify donor privacy or application quality;
- a black-box evaluation of one implementation is not an independent
  implementation;
- `world_truth` remains `NOT_EVALUATED` even if all unresolved entries are later
  removed by a justified amendment.

`validator/test_external_evaluation_trace.py` pins these boundaries and rejects
embedded domain verdicts and causal relationship vocabulary.

## Documents

- [CDTS in 60 seconds](spec/00_CDTS_IN_60_SECONDS.md)
- [Core](spec/01_CDTS_CORE.md)
- [Relationship vocabulary](spec/02_RELATIONSHIP_VOCABULARY.md)
- [Source revision policy](spec/03_SOURCE_REVISION_POLICY.md)
- [Conformance](spec/04_CONFORMANCE.md)
- [Pinned revisions](references/PINNED_SPEC_REVISIONS.md)
- [Resistance corpus](conformance/RESISTANCE_CORPUS.md)

MIT licensed. No multi-implementation conformance claim is made.
