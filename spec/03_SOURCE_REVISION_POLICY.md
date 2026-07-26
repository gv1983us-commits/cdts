# Source Revision Policy

A branch is a moving target; a 40-character commit revision is a fixed review object. CDTS uses one fixed revision per owner and fails closed on a missing, duplicated, mismatched, or wrong-owner pin.

Every owner represented in `record_refs` requires its pin. Review Protocol is always required with role `source_policy`. MPAA, BEC, and PCA pins use `normative_source` only to interpret their own referenced objects. ARB is optional and may use only `analytical_mapping`.

A record reference repeats its owner's pinned revision. The two values MUST match. This prevents a trace from silently combining interpretations from different source states.

The fixed candidate set is listed in `references/PINNED_SPEC_REVISIONS.md`. Changing any revision requires a new CDTS compatibility review and trace amendment; it is not a silent editorial update.
