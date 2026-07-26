# Cross-Domain Trace Set (CDTS)

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

## Documents

- [CDTS in 60 seconds](spec/00_CDTS_IN_60_SECONDS.md)
- [Core](spec/01_CDTS_CORE.md)
- [Relationship vocabulary](spec/02_RELATIONSHIP_VOCABULARY.md)
- [Source revision policy](spec/03_SOURCE_REVISION_POLICY.md)
- [Conformance](spec/04_CONFORMANCE.md)
- [Pinned revisions](references/PINNED_SPEC_REVISIONS.md)
- [Resistance corpus](conformance/RESISTANCE_CORPUS.md)

MIT licensed. No multi-implementation conformance claim is made.
