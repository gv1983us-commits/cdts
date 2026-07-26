# CDTS Contributor Instructions

Build and review this repository as a neutral public specification candidate. Use only the fixed public revisions listed in `references/PINNED_SPEC_REVISIONS.md`; never silently mix revisions.

Preserve ownership boundaries: external specifications own their records and conclusions; ARB is analytical only; Review Protocol owns source policy only; CDTS owns correlation trace structure and its own linkage assertions. Import the trace, not the conclusion.

Use strict RED-GREEN-REFACTOR for validator changes, standard-library Python, strict JSON parsing, schema/validator parity tests, and fail-closed validation. Public files must contain neutral infrastructure material only and no local paths, credentials, private links, private names, or internal correspondence.

Do not publish from an automated work session. Leave changes for human review.
