# CDTS Source Revision Policy

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
