# Conformance Corpus

Fixture names encode expectation: `valid-*`, `invalid-*`, and `malformed-*`. The corpus covers positive correlation, typed absence, unresolved relation, disclosed conflict, amendment history, full fixed-source coverage, dangling/self references, source and role mismatch, forbidden causal vocabulary, imported conclusions, conflict policy, incomplete unresolved state, unknown tokens, duplicate keys, and non-finite numbers.

Run `python -m unittest discover -v`. A third-party implementation should produce the same admissibility class or failure for every fixture before claiming v0.1 compatibility.
