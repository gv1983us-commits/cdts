# CDTS Core - Trace Profile v0.1-draft

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
