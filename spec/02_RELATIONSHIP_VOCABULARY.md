# CDTS Relationship Vocabulary v0.1

All tokens are CDTS-namespaced. They describe trace structure or temporal relation, not native domain conclusions.

## Structural

`cdts.references`, `cdts.derived_from`, `cdts.correlates`, `cdts.has_external_reference`, `cdts.has_transition_record`, `cdts.has_execution_record`.

## Temporal

`cdts.precedes`, `cdts.follows`, `cdts.co_occurs_with`, `cdts.overlaps`, `cdts.temporal_order_undetermined`.

## Boundary and support

`cdts.does_not_imply`, `cdts.conflicts_with`, `cdts.partially_supports`, `cdts.insufficient_for`.

Statuses are `cdts.observed`, `cdts.declared`, `cdts.derived`, `cdts.hypothesis`, `cdts.conflicting`, and `cdts.undetermined`. Bases are `cdts.explicit_reference`, `cdts.content_digest`, `cdts.timestamp_order`, `cdts.shared_receipt`, and `cdts.insufficient`.

v0.1 intentionally defines no causal relation. Sequence, overlap, shared scope, or shared references cannot establish causality, execution success, authorization, continuation, identity, or state commitment.
