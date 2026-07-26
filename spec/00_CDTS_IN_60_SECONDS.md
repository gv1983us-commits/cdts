# CDTS in 60 Seconds

A CDTS record correlates qualified references around one bounded **trace scope**. It does not declare that the references describe one real-world event.

Every external reference carries its owner, pinned specification revision, record type, owner-local identifier, location, SHA-256 digest, observation time, inbound link direction, and a non-import boundary. Owner-local IDs may repeat; CDTS `ref_id` values may not.

A `linkage_assertion` says only what CDTS can own: structural or temporal correlation. v0.1 has no causal vocabulary. Native conclusions stay behind the references.

Typed absence answers "why is a record not referenced?" Unresolved entries answer "what relationship remains unknown?" Conflicts preserve addressable positions; CDTS does not choose a winner without an external policy.

Validator output is derived, never producer-authored: `ADMISSIBLE`, variants for conflicts/unresolved, or `INVALID`. World truth is always `NOT_EVALUATED`.
