# CDTS Architectural Correction Gate

**Status:** local pre-publication review input
**Applies to:** CDTS v0.1-draft candidate

This gate corrects proposal-level assumptions against the pinned public revisions. A candidate is not acceptable merely because it implements the original handoff literally.

## Required corrections

1. **PCA provenance is not current ownership.** PCA v0.1 described a Linkage Record as an untested interpretive model. PCA v0.2 supersedes that Core and does not define a normative Linkage Record in its Core or schema. CDTS may attribute historical provenance but MUST define its own neutral `linkage_assertion` and MUST NOT present it as a current PCA object.
2. **ARB-04 is analytical.** It may be pinned with role `analytical_mapping`; it is not a normative dependency and does not authorize or validate CDTS relationships.
3. **Review Protocol owns source policy only.** CDTS architecture and proposals do not belong in the Review Protocol repository.
4. **A producer cannot self-award validation.** Admissibility is validator output. A persisted validation result, if later specified, must be a separate addressable attestation. External truth and authenticity remain `NOT_EVALUATED`.

## Required representation boundary

- Use `trace_scope` or `correlation_subject`, not event identity.
- Address external records by a qualified key containing owner, pinned revision, record type, and owner-local record ID.
- Carry location or content address, SHA-256 digest, link direction, and an explicit non-import boundary.
- Do not require bare owner-local IDs to be globally unique.
- Preserve native external conclusions without translating, recomputing, comparing, or selecting them.
- Treat conflicts as preserved positions. A local decision needs an external policy reference and does not erase the conflict.
- Use typed absence distinct from unresolved relations.

## v0.1 vocabulary boundary

CDTS v0.1 is limited to structural and temporal relationships. It MUST NOT define causal relationships such as `TRIGGERED_BY`, `CONTRIBUTED_TO`, or `REQUIRED_FOR` until a separate causal-evidence contract exists.

`same correlation scope`, shared timestamps, and shared evidence references do not imply mutual verification, causality, continuation, identity, authorization, execution success, or cross-step commitment.

## Validator judgments

The reference validator may establish only:

1. structural conformance;
2. local reference integrity and source-pin consistency;
3. admissibility of CDTS-owned boundary assertions.

It does not establish external record authenticity, evidence truth, world truth, or validity under the owning external specification.

## Publication gate

Public-facing files and fixtures must contain no private names, private project vocabulary, private or unrelated account identifiers, local paths, share links, secrets, or reconstructable private corpus. Public source coordinates MAY include the account identifiers required to address pinned public repositories. Examples should use neutral infrastructure scenarios.
