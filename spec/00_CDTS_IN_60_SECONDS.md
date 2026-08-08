# CDTS in 60 Seconds

**Artifact version:** `0.2`
**Record profile:** `0.1`
**Mode:** non-normative quick guide

A CDTS record correlates qualified references around one bounded trace scope. It does not declare that the references describe one real-world event.

Every external reference carries its owner, pinned specification revision, record type, owner-local identifier, location, SHA-256 digest, observation time, inbound link direction, and a non-import boundary. Owner-local IDs may repeat; CDTS `ref_id` values may not.

A `linkage_assertion` says only what CDTS can own: structural, temporal, boundary, or qualified-support correlation using CDTS-namespaced vocabulary. Profile v0.1 defines no causal relation. Native conclusions remain behind the references.

Typed absence explains a bounded non-reference state. Unresolved entries preserve unknown relations. Conflicts preserve independently addressable positions. CDTS does not choose a winner without an external precedence policy.

Validator output is derived, never producer-authored: `ADMISSIBLE`, qualified admissibility, `INVALID`, or tool failure. World truth is always `NOT_EVALUATED`.

The authority matrix and exact limits are in `../CANON.md`.
