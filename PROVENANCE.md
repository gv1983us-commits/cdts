# Cross-Domain Trace Set - Provenance

## 1. Repository authority

The authoritative public repository is:

```text
https://github.com/gv1983us-commits/cdts
```

A local copy, chat transcript, generated summary, House representation, or moving branch is not an exact source state without a commit pin.

## 2. Origin

CDTS emerged from the need to correlate addressable records owned by independent specifications without merging their claim domains or importing their conclusions.

One design precursor was the historical PCA v0.1 Linkage Record. The current PCA Core no longer owns that cross-domain object. CDTS defines its own independent `linkage_assertion` and does not present the historical PCA object as a current PCA norm.

## 3. Baseline and canonization

```text
initial public draft: d83d047b76cea174c6b4da2b666ed515a516110e
pre-canon main:       f91dbc003519efd5264655d905d0530dbfeac2fd
canonization date:    2026-08-06
```

The pre-canon repository already contained the v0.1 trace profile, schema, dependency-free validator, examples, resistance corpus, parity tests, publication checks, and an external-evaluation trace profile.

Canonization adds the artifact envelope, declares the five-surface authority matrix, updates the active compatibility set to accepted neighboring revisions, gives the schema a repository-owned public identity, and makes the artifact boundaries executable.

## 4. Version separation

```text
artifact version:       0.2-draft
record profile version: 0.1-draft
```

The artifact version changed because canon, provenance, relation, and compatibility surfaces changed. The record profile version did not change because the JSON record contract and token vocabulary remain profile v0.1-draft.

## 5. Human and tool participation

Repository history is the authority for commits and file changes. Human approval and governance remain distinct from model or automation assistance used to inspect, draft, transform, test, or publish repository content.

Tool participation does not establish authorship of external records, independent review, external execution, or world truth.

## 6. Historical review preservation

`review/TDD_LOG.md` and `review/ARCHITECTURAL_CORRECTION_GATE.md` remain historical development and review traces. Old source revisions inside historical records are not silently rewritten as if the earlier review had inspected later commits.

The active compatibility set is `references/PINNED_SPEC_REVISIONS.md`.

## 7. License

The repository publishes the MIT License in `LICENSE`.

## 8. Provenance limits

This provenance does not establish:

- identity or continuity of any model or agent;
- independence of implementations or evaluators;
- authenticity or completeness of referenced external records;
- causal connection among correlated records;
- external conformance;
- world truth.
