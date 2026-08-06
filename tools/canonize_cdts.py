#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD_TO_NEW = {
    "1d369f6cd091b99f9492cfaf730f0a170b55106e": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "bb46f5f8aac96d1cffba7a334c5d17fb331ef3af": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "6ad1a86d7c09b36839d162c580f84f05cfe4a598": "a669f023198615ad929f42df84f19380b57ca5ea",
    "595c08b877e4dfb14593454c2eec7c8f5df46c28": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "6b6c32cd467a4b5e4863d082b9da5bdd40d7dced": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
}

PINS = {
    "BEC": {
        "artifact_id": "claude.bec",
        "repository": "gv1983us-commits/behavioral-execution-contract",
        "revision": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
        "role": "normative_source",
    },
    "MPAA": {
        "artifact_id": "claude.mpaa",
        "repository": "gv1983us-commits/mpaa",
        "revision": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
        "role": "normative_source",
    },
    "PCA": {
        "artifact_id": "claude.pca",
        "repository": "gv1983us-commits/pca",
        "revision": "a669f023198615ad929f42df84f19380b57ca5ea",
        "role": "normative_source",
    },
    "REVIEW_PROTOCOL": {
        "artifact_id": "claude.review_protocol",
        "repository": "gv1983us-commits/repository-canon-review-protocol",
        "revision": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
        "role": "source_policy",
    },
    "ARB": {
        "artifact_id": "claude.arb",
        "repository": "gv1983us-commits/agent-runtime-boundaries",
        "revision": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
        "role": "analytical_mapping",
    },
}


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_pins(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in OLD_TO_NEW.items():
        updated = updated.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


for directory in (ROOT / "examples", ROOT / "conformance" / "fixtures"):
    for path in directory.glob("*.json"):
        replace_pins(path)
replace_pins(ROOT / "validator" / "cdts_validate.py")

schema_path = ROOT / "schema" / "cdts-record.schema.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
schema["$id"] = "https://raw.githubusercontent.com/gv1983us-commits/cdts/main/schema/cdts-record.schema.json"
schema["title"] = "Cross-Domain Trace Set record profile v0.1-draft"
schema["description"] = "A bounded correlation trace that imports qualified references, never external conclusions."
schema_path.write_text(json.dumps(schema, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

artifact = {
    "schema_version": "1.0",
    "artifact_id": "claude.cdts",
    "title": "Cross-Domain Trace Set",
    "repository": "gv1983us-commits/cdts",
    "artifact_version": "0.2-draft",
    "record_profile_version": "0.1-draft",
    "artifact_status": "canonical_public_draft",
    "license": "MIT",
    "claim_domain": "cross_domain_correlation_trace_admissibility",
    "normative_authority_model": "five_surface_domain_ownership_matrix",
    "normative_surface_count": 5,
    "normative_surfaces": [
        {"path": "spec/01_CDTS_CORE.md", "domain": "trace_semantics_ownership_boundaries_and_admissibility_requirements"},
        {"path": "spec/02_RELATIONSHIP_VOCABULARY.md", "domain": "cdts_namespaced_relationship_status_and_basis_meanings"},
        {"path": "spec/03_SOURCE_REVISION_POLICY.md", "domain": "owner_role_pin_and_compatibility_set_rules"},
        {"path": "spec/04_CONFORMANCE.md", "domain": "validation_pipeline_result_statuses_exit_codes_and_implementation_obligations"},
        {"path": "schema/cdts-record.schema.json", "domain": "record_profile_0_1_structural_representation"},
    ],
    "canonical_surfaces": {
        "human_entry": "README.md",
        "canon": "CANON.md",
        "machine_passport": "ARTIFACT.json",
        "relations": "RELATIONS.md",
        "provenance": "PROVENANCE.md",
        "normative_corpus": "spec/",
        "record_schema": "schema/cdts-record.schema.json",
        "compatibility_receipt": "references/PINNED_SPEC_REVISIONS.md",
        "conformance_corpus": "conformance/",
        "reference_implementation": "validator/",
        "verification": "review/",
    },
    "reference_implementation": {
        "path": "validator/cdts_validate.py",
        "normative": False,
        "role": "fail_closed_reference_validator",
    },
    "canonical_checks": [
        "python -m unittest discover -v",
        "python -m json.tool ARTIFACT.json >/dev/null",
        "python validator/cdts_validate.py examples/mpaa-bec-execution.json",
        "python -m review.test_artifact_canon",
    ],
    "result_statuses": [
        "ADMISSIBLE",
        "INVALID",
        "TOOL_FAILURE",
        "ADMISSIBLE_WITH_CONFLICTS",
        "ADMISSIBLE_WITH_UNRESOLVED",
        "ADMISSIBLE_WITH_CONFLICTS_AND_UNRESOLVED",
    ],
    "assertion_boundaries": {
        "event_identity_established": False,
        "causality_established": False,
        "external_conclusion_imported": False,
        "native_record_validity_established": False,
        "expected_record_completeness_evaluated": False,
        "external_authenticity_established": False,
        "external_producer_identity_or_distinctness_established": False,
        "predecessor_digest_correspondence_evaluated": False,
        "arb_normative_ownership_established": False,
        "neighbor_conformance_imported": False,
        "multi_implementation_conformance_claimed": False,
        "world_truth_evaluated": False,
    },
    "relations": [
        {
            "artifact_id": pin["artifact_id"],
            "repository": pin["repository"],
            "reviewed_revision": pin["revision"],
            "role": pin["role"],
            "conclusion_imported": False,
        }
        for pin in PINS.values()
    ],
}
(ROOT / "ARTIFACT.json").write_text(json.dumps(artifact, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

write("CANON.md", r'''# Cross-Domain Trace Set - Canon

**Artifact:** Cross-Domain Trace Set (CDTS)
**Corpus identity:** `claude.cdts`
**Repository:** `gv1983us-commits/cdts`
**Artifact version:** `0.2-draft`
**Record profile:** `0.1-draft`
**Canonical status:** `canonical_public_draft`
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
| Record Schema | `schema/cdts-record.schema.json` | structural representation of record profile `0.1-draft` |

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
''')

write("RELATIONS.md", r'''# Cross-Domain Trace Set - Relations

**Artifact:** `claude.cdts`
**Repository:** `gv1983us-commits/cdts`
**Relation mode:** fixed-revision compatibility review

CDTS records five independently pinned neighboring sources. Every relation keeps `conclusion_imported: false`.

## 1. BEC

```text
artifact_id: claude.bec
repository: gv1983us-commits/behavioral-execution-contract
reviewed_revision: 62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261
role: normative_source
conclusion_imported: false
```

CDTS may reference a BEC-owned execution record. It does not recompute BEC acceptance, trust-anchor sufficiency, authorization, invocation, evidence validity, or deployment level.

## 2. MPAA

```text
artifact_id: claude.mpaa
repository: gv1983us-commits/mpaa
reviewed_revision: 0d1aaf35cc4826622f3312fdd2a1c2d40890b965
role: normative_source
conclusion_imported: false
```

CDTS may reference an MPAA Runtime Report or other MPAA-owned record. It does not amend architecture, Identity Profile, Runtime Contract, Runtime Report, or MPAA conformance.

## 3. PCA

```text
artifact_id: claude.pca
repository: gv1983us-commits/pca
reviewed_revision: a669f023198615ad929f42df84f19380b57ca5ea
role: normative_source
conclusion_imported: false
```

CDTS may reference a PCA Transition Record. The historical PCA v0.1 Linkage Record is provenance for the CDTS design lineage, not a current PCA object imported into CDTS. CDTS does not establish process continuation, identity, or uninterrupted persistence.

## 4. Repository Canon and Review Protocol

```text
artifact_id: claude.review_protocol
repository: gv1983us-commits/repository-canon-review-protocol
reviewed_revision: b4205ffd91a6316ab40243cbf8161a1c512cae1f
role: source_policy
conclusion_imported: false
```

Review Protocol supplies fixed-source and review-discipline context. CDTS does not import donor-receipt validity, security, privacy, completeness, or external-execution conclusions.

## 5. ARB

```text
artifact_id: claude.arb
repository: gv1983us-commits/agent-runtime-boundaries
reviewed_revision: bcf9f628ee1d7c2075673b00f660674680bb6f62
role: analytical_mapping
conclusion_imported: false
```

ARB is analytical context only. It cannot be named as a normative owner of a CDTS assertion. CDTS admissibility does not make an ARB interpretation true, and ARB analysis does not validate a CDTS trace.

## 6. Reciprocal-revision rule

Relation records are independently pinned historical reviews. They are not required to point to one another's latest commit and do not form a recursive SHA fixpoint.

```text
exact reviewed revision != moving latest revision
reciprocal relation != identical review date
reference != conclusion import
```

## 7. Cross-domain rejection matrix

| Observed fact | Forbidden inference |
|---|---|
| two references share a scope | they describe one real-world event |
| timestamps are ordered | one event caused another |
| digests match | external authenticity or completeness is established |
| BEC record is referenced | BEC conclusion becomes a CDTS conclusion |
| PCA record is absent | process continuation failed |
| ARB is pinned | ARB is a normative dependency |
| trace is ADMISSIBLE | external records or world claims are true |
''')

write("PROVENANCE.md", r'''# Cross-Domain Trace Set - Provenance

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
''')

write("README.md", r'''# Cross-Domain Trace Set (CDTS)

[![CDTS checks](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml/badge.svg)](https://github.com/gv1983us-commits/cdts/actions/workflows/ci.yml)

**Artifact version:** `0.2-draft`
**Record profile:** `0.1-draft`
**Canonical status:** `canonical_public_draft`
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
| `schema/cdts-record.schema.json` | structural representation of record profile `0.1-draft` |

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
''')

write("AGENTS.md", r'''# CDTS Contributor Instructions

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
''')

write("spec/00_CDTS_IN_60_SECONDS.md", r'''# CDTS in 60 Seconds

**Artifact version:** `0.2-draft`
**Record profile:** `0.1-draft`
**Mode:** non-normative quick guide

A CDTS record correlates qualified references around one bounded trace scope. It does not declare that the references describe one real-world event.

Every external reference carries its owner, pinned specification revision, record type, owner-local identifier, location, SHA-256 digest, observation time, inbound link direction, and a non-import boundary. Owner-local IDs may repeat; CDTS `ref_id` values may not.

A `linkage_assertion` says only what CDTS can own: structural, temporal, boundary, or qualified-support correlation using CDTS-namespaced vocabulary. Profile v0.1 defines no causal relation. Native conclusions remain behind the references.

Typed absence explains a bounded non-reference state. Unresolved entries preserve unknown relations. Conflicts preserve independently addressable positions. CDTS does not choose a winner without an external precedence policy.

Validator output is derived, never producer-authored: `ADMISSIBLE`, qualified admissibility, `INVALID`, or tool failure. World truth is always `NOT_EVALUATED`.

The authority matrix and exact limits are in `../CANON.md`.
''')

write("spec/01_CDTS_CORE.md", r'''# CDTS Core - Trace Profile v0.1-draft

**Status:** normative
**Artifact version:** `0.2-draft`
**Normative domain:** trace semantics, ownership boundaries, and admissibility requirements

This document is one of five normative CDTS surfaces. It does not own token definitions, exact compatibility values, result exit codes, or JSON representation when those domains are assigned to another surface by `CANON.md`.

RFC 2119 terms are used in their ordinary standards sense.

**CDTS-CORE-001** A trace MUST identify one bounded correlation scope and MUST NOT represent that scope as event identity.

**CDTS-CORE-002** Every external record MUST use a unique local `ref_id` and a qualified external key: owner, pinned specification revision, record type, and owner-local record ID.

**CDTS-CORE-003** A reference MUST carry a stable location or content address, SHA-256 digest, timestamp, `external_to_cdts` direction, `trace_reference_only` boundary, and `conclusion_imported: false`.

**CDTS-CORE-004** Owner-local record IDs need not be globally unique. CDTS-local IDs MUST be unique.

**CDTS-CORE-005** The exact fixed revision of each represented owner MUST be listed. Review Protocol MUST be pinned as `source_policy`.

**CDTS-CORE-006** ARB MAY be listed only as `analytical_mapping`; it is not a normative dependency or owner of a CDTS assertion.

**CDTS-CORE-007** MPAA, BEC, and PCA retain sole authority for their record formats, validation, terms, and conclusions. CDTS MUST NOT represent an external conclusion as a CDTS-owned conclusion or translate, recompute, compare, or select it. The reference validator rejects dedicated conclusion fields but does not semantically classify free-text values; semantic compliance of free text is `NOT_EVALUATED` and requires separate review.

**CDTS-CORE-008** PCA's historical Linkage Record does not become a CDTS object. The accepted PCA Core has no current normative Linkage Record. CDTS defines a separate `linkage_assertion`.

**CDTS-CORE-009** Link endpoints and evidence references MUST resolve to local `ref_id` values. Self-links are forbidden.

**CDTS-CORE-010** Any absence represented by CDTS MUST use a typed state: `not_applicable`, `not_observed`, `not_produced`, `unavailable`, or `undetermined`, with a reason. Profile v0.1 does not define an expected-record universe and does not evaluate record-set completeness.

**CDTS-CORE-011** Unresolved relations MUST remain explicit and identify required evidence and affected linkages.

**CDTS-CORE-012** Conflicts MUST preserve independently addressable position digests. A local choice MUST cite an external precedence policy and MUST NOT erase disclosure.

**CDTS-CORE-013** Temporal order MUST agree with known timestamps. Temporal correlation MUST NOT be promoted to causality.

**CDTS-CORE-014** Trace provenance MUST identify its producer with a qualified identifier and role `coordination_layer`. Producer-authored validation fields are forbidden. External record producer identity and distinctness are `NOT_EVALUATED` unless supplied by a separate addressable attestation.

**CDTS-CORE-015** Amendments MUST form a contiguous chain from revision 1 and carry a syntactically valid claimed digest for each previous trace revision. The single-record validator does not retrieve predecessor artifacts, so previous-digest correspondence is `NOT_EVALUATED`.

**CDTS-CORE-016** Implementations MUST reject duplicate JSON keys, non-finite numbers, invalid UTF-8, unknown normative tokens, and unsupported normative schema assertions.

**CDTS-CORE-017** Admissibility establishes only machine-checkable CDTS structural, local-reference, source-pin, and boundary conformance. Free-text semantics, expected-record completeness, predecessor-digest correspondence, external producer identity, authenticity, external validation, causality, identity, and world truth are not evaluated.

## Data model

The root consists of version and revision identity; `trace_scope`; fixed `source_revisions`; qualified `record_refs`; typed `absences`; CDTS-owned `linkage_assertions`; `conflicts`; `unresolved`; producer `provenance`; and `amendments`.

The JSON Schema owns structural representation. Cross-reference, source-pin, temporal, ownership, conflict-policy, amendment, and derived-status checks are operationalized by the reference validator under Core, Source Revision Policy, Relationship Vocabulary, and Conformance.
''')

write("spec/02_RELATIONSHIP_VOCABULARY.md", r'''# CDTS Relationship Vocabulary - Profile v0.1

**Status:** normative
**Artifact version:** `0.2-draft`
**Normative domain:** meanings of CDTS-namespaced relationship, assertion-status, and basis tokens

All tokens describe CDTS trace structure or qualified relation. They are not native domain conclusions.

## Structural relationships

`cdts.references`, `cdts.derived_from`, `cdts.correlates`, `cdts.has_external_reference`, `cdts.has_transition_record`, `cdts.has_execution_record`.

## Temporal relationships

`cdts.precedes`, `cdts.follows`, `cdts.co_occurs_with`, `cdts.overlaps`, `cdts.temporal_order_undetermined`.

## Boundary and support relationships

`cdts.does_not_imply`, `cdts.conflicts_with`, `cdts.partially_supports`, `cdts.insufficient_for`.

`cdts.partially_supports` means only that cited evidence supports a bounded CDTS assertion under the stated basis. It does not import or validate the external domain conclusion.

## Assertion statuses

`cdts.observed`, `cdts.declared`, `cdts.derived`, `cdts.hypothesis`, `cdts.conflicting`, and `cdts.undetermined`.

## Bases

`cdts.explicit_reference`, `cdts.content_digest`, `cdts.timestamp_order`, `cdts.shared_receipt`, and `cdts.insufficient`.

Profile v0.1 intentionally defines no causal relationship. Sequence, overlap, shared scope, matching digest, or shared receipt cannot establish causality, execution success, authorization, continuation, identity, authenticity, completeness, or state commitment.
''')

write("spec/03_SOURCE_REVISION_POLICY.md", r'''# CDTS Source Revision Policy

**Status:** normative
**Artifact version:** `0.2-draft`
**Normative domain:** owner, role, exact-pin, record-reference parity, and compatibility-set change rules

A branch is a moving target; a 40-character commit revision is a fixed review object.

CDTS uses one fixed revision per owner and fails closed on a missing, duplicated, mismatched, wrong-owner, or wrong-role pin.

Every owner represented in `record_refs` requires its pin. Review Protocol is always required with role `source_policy`. MPAA, BEC, and PCA use `normative_source` only to interpret their own referenced objects. ARB is optional and may use only `analytical_mapping`.

A record reference repeats its owner's pinned revision. The two values MUST match. This prevents one trace from silently combining interpretations from different source states.

## Compatibility receipt

The exact reviewed values for the current artifact revision are recorded in `../references/PINNED_SPEC_REVISIONS.md`.

That file is a canonical compatibility receipt, not a sixth abstract normative surface. This policy owns the requirement for an exact declared set; the receipt records the accepted values.

Changing any owner, repository, role, or revision requires:

1. an explicit compatibility review against the new fixed source;
2. updates to validator pins, examples, and fixtures;
3. a new artifact revision and provenance entry;
4. no rewriting of historical review records as though they inspected the new revision.

Reciprocal relation files are independent historical reviews and need not point to one another's latest commits.
''')

write("spec/04_CONFORMANCE.md", r'''# CDTS Conformance - Profile v0.1

**Status:** normative
**Artifact version:** `0.2-draft`
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
''')

write("references/PINNED_SPEC_REVISIONS.md", r'''# CDTS Compatibility Receipt - Accepted Neighbor Revisions

**Artifact version:** `0.2-draft`
**Record profile:** `0.1-draft`
**Review date:** 2026-08-06
**Receipt role:** exact fixed-source compatibility evidence; not a sixth normative surface

The current candidate was reviewed and tested against exactly these public revisions:

| Owner | Repository | Revision | Role |
|---|---|---|---|
| BEC | `gv1983us-commits/behavioral-execution-contract` | `62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261` | `normative_source` |
| MPAA | `gv1983us-commits/mpaa` | `0d1aaf35cc4826622f3312fdd2a1c2d40890b965` | `normative_source` |
| PCA | `gv1983us-commits/pca` | `a669f023198615ad929f42df84f19380b57ca5ea` | `normative_source` |
| Review Protocol | `gv1983us-commits/repository-canon-review-protocol` | `b4205ffd91a6316ab40243cbf8161a1c512cae1f` | `source_policy` |
| ARB | `gv1983us-commits/agent-runtime-boundaries` | `bcf9f628ee1d7c2075673b00f660674680bb6f62` | `analytical_mapping` |

ARB neither authorizes nor validates a CDTS assertion. Review Protocol owns review discipline, not CDTS architecture. MPAA, BEC, and PCA remain authoritative only for their own objects and conclusions.

Pins MUST NOT be updated without explicit compatibility review. Historical review files retain the revisions they actually inspected.
''')

write("validator/README.md", r'''# CDTS Reference Validator

The validator implements record profile `0.1-draft` for artifact version `0.2-draft`.

It uses only the Python standard library at runtime.

```bash
python validator/cdts_validate.py path/to/trace.json
python validator/cdts_validate.py --json path/to/trace.json
python -m unittest discover -v
```

The validator loads the normative schema, supports a deliberately bounded audited JSON Schema keyword subset, and treats unsupported normative assertions as tool failure.

Its result is derived; a trace cannot contain a producer-authored validation field.

The validator is a reference implementation, not a sixth normative surface. External authenticity, native-spec validity, expected-record completeness, producer identity, causality, identity, and world truth are outside its result.
''')

write("conformance/README.md", r'''# CDTS Conformance Corpus

This directory provides executable evidence for record profile `0.1-draft` under artifact version `0.2-draft`.

- `fixtures/valid-*.json` must produce an admissible or qualified-admissible result.
- `fixtures/invalid-*.json` must produce `INVALID`.
- `fixtures/malformed-*.json` must fail strict parsing.
- `RESISTANCE_CORPUS.md` explains the overclaim classes resisted by the fixtures.

The corpus is not a normative sixth surface and does not establish multi-implementation conformance, external record validity, or world truth.
''')

write("review/PUBLICATION_MANIFEST.md", r'''# CDTS Publication Manifest

**Candidate:** CDTS artifact `0.2-draft`
**Record profile:** `0.1-draft`
**Status:** `canonical_public_draft`
**Prepared:** 2026-08-06
**Normative surfaces:** 5

## Canonical envelope

- `README.md`
- `CANON.md`
- `ARTIFACT.json`
- `RELATIONS.md`
- `PROVENANCE.md`

## Normative surfaces

- `spec/01_CDTS_CORE.md`
- `spec/02_RELATIONSHIP_VOCABULARY.md`
- `spec/03_SOURCE_REVISION_POLICY.md`
- `spec/04_CONFORMANCE.md`
- `schema/cdts-record.schema.json`

## Non-normative but canonical support surfaces

- `spec/00_CDTS_IN_60_SECONDS.md`
- `references/PINNED_SPEC_REVISIONS.md`
- `validator/`
- `conformance/`
- `examples/`
- `review/`

## Current compatibility set

```text
BEC             62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261
MPAA            0d1aaf35cc4826622f3312fdd2a1c2d40890b965
PCA             a669f023198615ad929f42df84f19380b57ca5ea
Review Protocol b4205ffd91a6316ab40243cbf8161a1c512cae1f
ARB             bcf9f628ee1d7c2075673b00f660674680bb6f62
```

## Required gates

- `ARTIFACT.json` parses and declares exactly five normative surfaces;
- schema has a repository-owned public `$id`;
- validator, receipt, examples, and fixtures use the current compatibility set;
- every relation keeps `conclusion_imported: false`;
- the complete unit, parity, publication, and canon suite passes;
- canonical examples produce expected admissibility results;
- causal relationship tokens remain absent from profile v0.1;
- public files contain no local path, private share link, or credential marker;
- GitHub Actions are pinned and pass on Python 3.10 through 3.13;
- MIT remains tied to `LICENSE`.

Passing publication gates does not establish external authenticity, completeness, identity, causality, neighboring conformance, or world truth.
''')

write("review/2026-08-06_CANONIZATION_REVIEW.md", r'''# CDTS Canonization Review - 2026-08-06

**Repository:** `gv1983us-commits/cdts`
**Starting revision:** `f91dbc003519efd5264655d905d0530dbfeac2fd`
**Review mode:** fixed-revision artifact canonization

## Findings

1. The v0.1 technical body was already strong: strict parser, structural schema, fail-closed validator, parity tests, resistance corpus, examples, and four-version CI.
2. Normative authority was not explicitly distributed even though obligations existed in Core, Vocabulary, Source Revision Policy, Conformance, and Schema.
3. The active compatibility set still referenced July revisions of all five neighboring artifacts.
4. The schema `$id` used `example.org` rather than a repository-owned public identity.
5. The repository lacked a complete canon, machine passport, relation surface, and provenance declaration.

## Corrections

- declared a five-surface domain-ownership matrix;
- kept record profile `0.1-draft` while advancing artifact version to `0.2-draft`;
- classified the compatibility receipt as exact evidence, not a sixth normative surface;
- updated all active pins in the validator, receipt, examples, and fixtures;
- assigned the schema a repository-owned public `$id`;
- added `CANON.md`, `ARTIFACT.json`, `RELATIONS.md`, and `PROVENANCE.md`;
- added executable artifact-canon checks;
- preserved historical TDD and correction records without rewriting old reviewed revisions.

## Boundary result

```text
ADMISSIBLE trace != external conclusion
correlation != event identity
ordered time != causality
matching digest != authenticity or completeness
ARB mapping != normative ownership
validator output != world truth
```

No independent multi-implementation conformance claim is made.
''')

write("review/test_artifact_canon.py", r'''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "ARTIFACT.json"
CANON = ROOT / "CANON.md"
RELATIONS = ROOT / "RELATIONS.md"
PROVENANCE = ROOT / "PROVENANCE.md"
RECEIPT = ROOT / "references" / "PINNED_SPEC_REVISIONS.md"

EXPECTED_SURFACES = {
    "spec/01_CDTS_CORE.md",
    "spec/02_RELATIONSHIP_VOCABULARY.md",
    "spec/03_SOURCE_REVISION_POLICY.md",
    "spec/04_CONFORMANCE.md",
    "schema/cdts-record.schema.json",
}
EXPECTED_RELATIONS = {
    "claude.bec": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "claude.mpaa": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "claude.pca": "a669f023198615ad929f42df84f19380b57ca5ea",
    "claude.review_protocol": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "claude.arb": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
}


class ArtifactCanonTests(unittest.TestCase):
    def artifact(self):
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_identity_and_versions(self):
        artifact = self.artifact()
        self.assertEqual(artifact["artifact_id"], "claude.cdts")
        self.assertEqual(artifact["repository"], "gv1983us-commits/cdts")
        self.assertEqual(artifact["artifact_version"], "0.2-draft")
        self.assertEqual(artifact["record_profile_version"], "0.1-draft")
        self.assertEqual(artifact["artifact_status"], "canonical_public_draft")
        self.assertEqual(artifact["license"], "MIT")

    def test_five_surface_authority_matrix(self):
        artifact = self.artifact()
        self.assertEqual(artifact["normative_authority_model"], "five_surface_domain_ownership_matrix")
        self.assertEqual(artifact["normative_surface_count"], 5)
        self.assertEqual({item["path"] for item in artifact["normative_surfaces"]}, EXPECTED_SURFACES)
        self.assertFalse(artifact["reference_implementation"]["normative"])
        self.assertNotIn("references/PINNED_SPEC_REVISIONS.md", EXPECTED_SURFACES)

    def test_five_relations_are_exact_and_non_importing(self):
        relations = {item["artifact_id"]: item for item in self.artifact()["relations"]}
        self.assertEqual(set(relations), set(EXPECTED_RELATIONS))
        for artifact_id, revision in EXPECTED_RELATIONS.items():
            with self.subTest(artifact_id=artifact_id):
                self.assertEqual(relations[artifact_id]["reviewed_revision"], revision)
                self.assertFalse(relations[artifact_id]["conclusion_imported"])

    def test_all_assertion_boundaries_remain_false(self):
        boundaries = self.artifact()["assertion_boundaries"]
        self.assertTrue(boundaries)
        self.assertTrue(all(value is False for value in boundaries.values()))

    def test_human_surfaces_publish_core_boundaries(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (CANON, RELATIONS, PROVENANCE, RECEIPT)
        )
        for marker in (
            "normative_surface_count = 5",
            "not a sixth",
            "conclusion_imported: false",
            "correlation != event identity",
            "sequence != causality",
            "world truth",
            "reciprocal",
        ):
            self.assertIn(marker.lower(), combined.lower())

    def test_schema_identity_is_repository_owned(self):
        schema = json.loads((ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            schema["$id"],
            "https://raw.githubusercontent.com/gv1983us-commits/cdts/main/schema/cdts-record.schema.json",
        )
        self.assertEqual(schema["properties"]["cdts_version"]["const"], "0.1-draft")


if __name__ == "__main__":
    unittest.main()
''')

write("review/test_publication.py", r'''"""Publication and boundary checks for the canonical CDTS artifact."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from validator.cdts_validate import PINNED_SOURCES, parse_json_bytes, validate_file

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "CANON.md", "ARTIFACT.json", "RELATIONS.md", "PROVENANCE.md", "LICENSE",
    "spec/00_CDTS_IN_60_SECONDS.md", "spec/01_CDTS_CORE.md",
    "spec/02_RELATIONSHIP_VOCABULARY.md", "spec/03_SOURCE_REVISION_POLICY.md",
    "spec/04_CONFORMANCE.md", "schema/cdts-record.schema.json",
    "validator/cdts_validate.py", "validator/README.md", "validator/test_validator.py",
    "validator/test_schema_parity.py", "validator/test_external_evaluation_trace.py",
    "conformance/README.md", "conformance/RESISTANCE_CORPUS.md",
    "examples/mpaa-bec-execution.json", "examples/mpaa-pca-host-transition.json",
    "examples/full-cross-domain-event.json", "examples/external-evaluation-run.json",
    "references/PINNED_SPEC_REVISIONS.md", "review/TDD_LOG.md",
    "review/ARCHITECTURAL_CORRECTION_GATE.md", "review/PUBLICATION_MANIFEST.md",
    "review/2026-08-06_CANONIZATION_REVIEW.md", "review/test_artifact_canon.py",
    ".github/workflows/ci.yml", ".gitignore",
}
PUBLIC_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}
EXPECTED_PINS = {
    "MPAA": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "BEC": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "PCA": "a669f023198615ad929f42df84f19380b57ca5ea",
    "REVIEW_PROTOCOL": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "ARB": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
}


def public_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path


class PublicationTests(unittest.TestCase):
    def test_required_artifacts_exist(self):
        self.assertEqual([], sorted(name for name in REQUIRED if not (ROOT / name).is_file()))

    def test_readme_declares_canonical_public_draft(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("canonical_public_draft", readme)
        self.assertIn("Artifact version", readme)
        self.assertIn("Record profile", readme)
        self.assertNotIn("unpublished candidate", readme)

    def test_all_machine_json_is_strict(self):
        for path in ROOT.rglob("*.json"):
            if "malformed-" in path.name:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                parse_json_bytes(path.read_bytes())

    def test_examples_and_positive_fixtures_are_admissible(self):
        paths = list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("valid-*.json"))
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotEqual("INVALID", validate_file(path).status)

    def test_current_pins_are_consistent_everywhere_active(self):
        self.assertEqual({owner: value[1] for owner, value in PINNED_SOURCES.items()}, EXPECTED_PINS)
        receipt = (ROOT / "references" / "PINNED_SPEC_REVISIONS.md").read_text(encoding="utf-8")
        for owner, revision in EXPECTED_PINS.items():
            self.assertIn(revision, receipt, owner)
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("*.json")):
            if path.name.startswith("malformed-"):
                continue
            text = path.read_text(encoding="utf-8")
            for old in (
                "1d369f6cd091b99f9492cfaf730f0a170b55106e",
                "bb46f5f8aac96d1cffba7a334c5d17fb331ef3af",
                "6ad1a86d7c09b36839d162c580f84f05cfe4a598",
                "595c08b877e4dfb14593454c2eec7c8f5df46c28",
                "6b6c32cd467a4b5e4863d082b9da5bdd40d7dced",
            ):
                self.assertNotIn(old, text, str(path.relative_to(ROOT)))

    def test_no_local_paths_private_links_or_credentials(self):
        forbidden = re.compile(
            r"(C:\\Users\\|/Users/|/home/|chatgpt\.com/share/|localhost:|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|ghp_[A-Za-z0-9]+|"
            r"github_pat_[A-Za-z0-9_]+|(?<![A-Za-z0-9])sk-[A-Za-z0-9]+)",
            re.IGNORECASE,
        )
        for path in public_files():
            if path.resolve() == Path(__file__).resolve():
                continue
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), str(path.relative_to(ROOT)))

    def test_public_surface_is_ascii(self):
        for path in public_files():
            if path.name.startswith("test_") or path.name == "cdts_validate.py":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[^\x00-\x7f]", text), str(path.relative_to(ROOT)))

    def test_no_producer_authored_validation_surface(self):
        schema = json.loads((ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("validation", schema["properties"])
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("valid-*.json")):
            self.assertNotIn("validation", json.loads(path.read_text(encoding="utf-8")))

    def test_profile_v01_has_no_causal_relationship_tokens(self):
        schema_text = (ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8").lower()
        for token in ("triggered_by", "contributed_to", "required_for"):
            self.assertNotIn(token, schema_text)

    def test_normative_boundaries_match_machine_surface(self):
        artifact = json.loads((ROOT / "ARTIFACT.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["normative_surface_count"], 5)
        self.assertFalse(artifact["reference_implementation"]["normative"])
        self.assertTrue(all(value is False for value in artifact["assertion_boundaries"].values()))

    def test_github_actions_are_pinned_by_commit(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        uses = re.findall(r"^\s*(?:-\s+)?uses:\s+([^\s#]+)", workflow, flags=re.MULTILINE)
        self.assertGreater(len(uses), 0)
        for action in uses:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_license_is_declared_and_present(self):
        artifact = json.loads((ROOT / "ARTIFACT.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["license"], "MIT")
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
''')

write(".github/workflows/ci.yml", r'''name: CDTS checks

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    name: Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    timeout-minutes: 10
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]

    steps:
      - name: Check out repository
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4

      - name: Set up Python
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install test-only schema oracle
        run: python -m pip install "jsonschema>=4.20,<5"

      - name: Validate machine passport
        run: python -m json.tool ARTIFACT.json >/dev/null

      - name: Compile validator and checks
        run: python -m compileall -q validator review

      - name: Run complete test suite
        run: python -m unittest discover -v

      - name: Run artifact canon explicitly
        run: python -m review.test_artifact_canon

      - name: Validate canonical example
        run: python validator/cdts_validate.py examples/mpaa-bec-execution.json

      - name: Validate external evaluation example
        shell: bash
        run: |
          set +e
          output=$(python validator/cdts_validate.py examples/external-evaluation-run.json --json)
          code=$?
          if [ "$code" -ne 4 ]; then
            echo "Expected ADMISSIBLE_WITH_UNRESOLVED exit 4, got $code" >&2
            echo "$output" >&2
            exit 1
          fi
          python -c 'import json,sys; p=json.loads(sys.stdin.read()); assert p["status"]=="ADMISSIBLE_WITH_UNRESOLVED"; assert p["world_truth"]=="NOT_EVALUATED"' <<<"$output"
''')

print("CDTS canonization migration applied")
