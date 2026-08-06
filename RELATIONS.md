# Cross-Domain Trace Set - Relations

**Artifact:** `claude.cdts`
**Repository:** `gv1983us-commits/cdts`
**Relation mode:** fixed-revision compatibility review

CDTS records five independently pinned neighboring sources. Every relation keeps `conclusion_imported: false`.

## 1. BEC

```text
artifact_id: claude.bec
repository: gv1983us-commits/behavioral-execution-contract
reviewed_revision: 62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261
role: normative_source
conclusion_imported: false
```

CDTS may reference a BEC-owned execution record. It does not recompute BEC acceptance, trust-anchor sufficiency, authorization, invocation, evidence validity, or deployment level.

## 2. MPAA

```text
artifact_id: claude.mpaa
repository: gv1983us-commits/mpaa
reviewed_revision: 0d1aaf35cc4826622f3312fdd2a1c2d40890b965
role: normative_source
conclusion_imported: false
```

CDTS may reference an MPAA Runtime Report or other MPAA-owned record. It does not amend architecture, Identity Profile, Runtime Contract, Runtime Report, or MPAA conformance.

## 3. PCA

```text
artifact_id: claude.pca
repository: gv1983us-commits/pca
reviewed_revision: a669f023198615ad929f42df84f19380b57ca5ea
role: normative_source
conclusion_imported: false
```

CDTS may reference a PCA Transition Record. The historical PCA v0.1 Linkage Record is provenance for the CDTS design lineage, not a current PCA object imported into CDTS. CDTS does not establish process continuation, identity, or uninterrupted persistence.

## 4. Repository Canon and Review Protocol

```text
artifact_id: claude.review_protocol
repository: gv1983us-commits/repository-canon-review-protocol
reviewed_revision: b4205ffd91a6316ab40243cbf8161a1c512cae1f
role: source_policy
conclusion_imported: false
```

Review Protocol supplies fixed-source and review-discipline context. CDTS does not import donor-receipt validity, security, privacy, completeness, or external-execution conclusions.

## 5. ARB

```text
artifact_id: claude.arb
repository: gv1983us-commits/agent-runtime-boundaries
reviewed_revision: bcf9f628ee1d7c2075673b00f660674680bb6f62
role: analytical_mapping
conclusion_imported: false
```

ARB is analytical context only. It cannot be named as a normative owner of a CDTS assertion. CDTS admissibility does not make an ARB interpretation true, and ARB analysis does not validate a CDTS trace.

## 6. Reciprocal-revision rule

Relation records are independently pinned historical reviews. They are not required to point to one another's latest commit and do not form a recursive SHA fixpoint.

```text
exact reviewed revision != moving latest revision
reciprocal relation != identical review date
reference != conclusion import
```

## 7. Cross-domain rejection matrix

| Observed fact | Forbidden inference |
|---|---|
| two references share a scope | they describe one real-world event |
| timestamps are ordered | one event caused another |
| digests match | external authenticity or completeness is established |
| BEC record is referenced | BEC conclusion becomes a CDTS conclusion |
| PCA record is absent | process continuation failed |
| ARB is pinned | ARB is a normative dependency |
| trace is ADMISSIBLE | external records or world claims are true |
