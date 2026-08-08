# CDTS Relationship Vocabulary - Profile v0.1

**Status:** normative
**Artifact version:** `0.2`
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
