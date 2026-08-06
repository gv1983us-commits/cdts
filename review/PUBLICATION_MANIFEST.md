# CDTS Publication Manifest

**Candidate:** CDTS artifact `0.2-draft`
**Record profile:** `0.1-draft`
**Status:** `canonical_public_draft`
**Prepared:** 2026-08-06
**Normative surfaces:** 5

## Canonical envelope

- `README.md`
- `CANON.md`
- `ARTIFACT.json`
- `RELATIONS.md`
- `PROVENANCE.md`

## Normative surfaces

- `spec/01_CDTS_CORE.md`
- `spec/02_RELATIONSHIP_VOCABULARY.md`
- `spec/03_SOURCE_REVISION_POLICY.md`
- `spec/04_CONFORMANCE.md`
- `schema/cdts-record.schema.json`

## Non-normative but canonical support surfaces

- `spec/00_CDTS_IN_60_SECONDS.md`
- `references/PINNED_SPEC_REVISIONS.md`
- `validator/`
- `conformance/`
- `examples/`
- `review/`

## Current compatibility set

```text
BEC             62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261
MPAA            0d1aaf35cc4826622f3312fdd2a1c2d40890b965
PCA             a669f023198615ad929f42df84f19380b57ca5ea
Review Protocol b4205ffd91a6316ab40243cbf8161a1c512cae1f
ARB             bcf9f628ee1d7c2075673b00f660674680bb6f62
```

## Required gates

- `ARTIFACT.json` parses and declares exactly five normative surfaces;
- schema has a repository-owned public `$id`;
- validator, receipt, examples, and fixtures use the current compatibility set;
- every relation keeps `conclusion_imported: false`;
- the complete unit, parity, publication, and canon suite passes;
- canonical examples produce expected admissibility results;
- causal relationship tokens remain absent from profile v0.1;
- public files contain no local path, private share link, or credential marker;
- GitHub Actions are pinned and pass on Python 3.10 through 3.13;
- MIT remains tied to `LICENSE`.

Passing publication gates does not establish external authenticity, completeness, identity, causality, neighboring conformance, or world truth.
