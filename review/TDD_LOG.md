# TDD Log

This log records commands actually executed while building the local candidate. Output is abbreviated only where noted; counts and failure causes are preserved.

## Initial RED

Command:

```text
python -m unittest validator.test_validator validator.test_schema_parity
```

Actual result:

```text
Ran 2 tests in 0.001s
FAILED (errors=2)
ModuleNotFoundError: No module named 'validator.cdts_validate'
```

The tests existed first and failed because the validator module did not exist.

## First GREEN attempt and focused correction

After the first schema and validator implementation, the same command produced:

```text
Ran 36 tests in 0.238s
FAILED (failures=2)
```

Both failures showed that `oneOf` hid precise `SCHEMA_PATTERN` and `SCHEMA_TYPE` diagnostics. The discriminator handling was corrected. Re-running produced:

```text
Ran 36 tests in 0.105s
OK
```

## Fixed-source architectural correction RED

A pinned-source review introduced `review/ARCHITECTURAL_CORRECTION_GATE.md` and replaced proposal-level tests with the corrected representation boundary. Full discovery then produced:

```text
Ran 34 tests in 0.121s
FAILED (failures=24, errors=6)
```

The failures were expected: the old implementation used event identity, unqualified domain slots, producer-authored validation, unnamespaced/causal vocabulary, and treated the PCA Linkage Record as current. The implementation and schema were replaced rather than patched around those assumptions.

## Corrected GREEN

Focused command:

```text
python -m unittest validator.test_validator.StrictParsingTests validator.test_validator.BoundaryTests validator.test_schema_parity -v
```

Actual result:

```text
Ran 32 tests in 0.146s
OK
```

After regenerating the conformance corpus and examples:

```text
python -m unittest discover -v
Ran 34 tests in 0.230s
OK
```

Final verification:

```text
python -m py_compile validator/cdts_validate.py validator/test_validator.py validator/test_schema_parity.py review/test_publication.py
(no output; exit 0)

python -m unittest discover
Ran 42 tests in 0.244s
OK

python -m review.test_publication
Ran 8 tests in 0.090s
OK
```

The final corpus sweep processed 24 JSON inputs (21 fixtures and 3 examples): 7 `ADMISSIBLE`, 1 `ADMISSIBLE_WITH_CONFLICTS`, 1 `ADMISSIBLE_WITH_UNRESOLVED`, 12 `INVALID`, and 3 strict parse failures, with zero expectation mismatches.

## Independent boundary-audit RED/GREEN cycles

A later boundary audit added one focused regression at a time and executed each regression before and after the minimal implementation change:

1. JSON Schema equality at the non-import boundary: Python's `True == 1` behavior caused a RED false accept for `conclusion_imported: 1`; a JSON-value-aware equality function made the focused test GREEN.
2. Conflict participant correspondence: duplicated position references left one declared conflict participant uncovered; the focused test was RED until the validator required exact correspondence between `record_refs` and `positions[].record_ref`.
3. Precedence-policy addressability: `precedence_policy_ref: "x"` was accepted; the focused test was RED until the schema required a URI-scheme-qualified reference.
4. Draft 2020-12 integer parity: `trace_revision: 1.0` was falsely rejected; the focused test was RED until finite integer-valued JSON numbers were accepted as schema integers.
5. In-memory fail-closed behavior: a non-JSON `set()` inside `evidence_refs` raised during uniqueness checking; the focused test was RED until pairwise JSON-aware comparison replaced serialization-based comparison.
6. Canonical timestamp syntax: compact and offset timestamps were accepted by the hand-written subset; the focused test was RED until the canonical schema required UTC `...Z` syntax.

Post-resume verification of the last focused regression:

```text
python -m unittest validator.test_validator.BoundaryTests.test_scope_and_provenance_time_are_ordered -v
Ran 1 test
OK
```

Fresh complete verification after all six cycles:

```text
python -m py_compile validator/cdts_validate.py validator/test_validator.py validator/test_schema_parity.py review/test_publication.py
(no output; exit 0)

python -m unittest discover -v
Ran 45 tests
OK

python -m review.test_publication
Ran 8 tests
OK
```

## CI dependency pinning RED/GREEN

The publication boundary was extended to require every GitHub Action dependency to use an immutable 40-character commit SHA. The focused test was executed before the workflow edit:

```text
python -m unittest review.test_publication.PublicationTests.test_github_actions_are_pinned_by_commit -v
FAILED (failures=2)
actions/checkout@v4
actions/setup-python@v5
```

The current official major-tag commits were resolved through the GitHub API, then the workflow was minimally pinned while retaining major-version comments. The same focused test was rerun:

```text
Ran 1 test
OK
```

## Stable pre-review gate

The complete candidate tree was hashed immediately before and after one fresh-process gate; all tracked and intended files were byte-identical across execution.

```text
python -m py_compile validator/cdts_validate.py validator/test_validator.py validator/test_schema_parity.py review/test_publication.py
(no output; exit 0)

python -m unittest discover -v
Ran 46 tests
OK

python -m review.test_publication
Ran 9 tests
OK
```

An isolated Draft 2020-12 oracle with format validation executed 17 differential mutations with zero custom-validator mismatches. The process-level CLI matrix executed six cases with zero exit-code or JSON-output mismatches. The 24-input corpus matrix retained zero expectation mismatches. A session-specific disclosure scan inspected 48 text files with zero hits. Trivy reported no HIGH or CRITICAL vulnerability, misconfiguration, or secret findings in the source tree.

## Independent staged-tree audit corrections

Two independent reviewers audited immutable staged tree `5d68694c8358badd7384a5a0bdc7dbf13be8d119`. The full fail-closed review read all 48 tracked files, reran the baseline and executable mutations, and returned `FAILED` with no P0 findings. The correction pass used one focused RED before each behavioral change:

1. External location addressability: `location: "x"` returned `ADMISSIBLE`; the new regression failed until the schema required an absolute URI-scheme-qualified location.
2. Producer addressability: `produced_by: "MPAA"` returned `ADMISSIBLE`; the new regression failed until provenance required a qualified producer identifier.
3. Normative-machine parity: a publication regression failed while Core overclaimed expected-record completeness, external-producer distinctness, predecessor-digest correspondence, and semantic inspection of free text. Core, Conformance, the resistance corpus, README, and publication gate were narrowed to the machine-checkable boundary; public owner identifiers remain permitted only as required public source coordinates.
4. Failure-result consistency: malformed JSON CLI output omitted `world_truth`; the focused test raised `KeyError` until parse and schema failure payloads both reported `NOT_EVALUATED`.
5. Malformed supported schema assertions: eight malformed keyword-value mutations all passed `load_schema()` during RED. Loader preflight now validates supported keyword shapes, local references, types, formats, numeric bounds, and regular expressions before data validation; all eight cases are GREEN.

## Post-audit verification

The first complete post-fix gate completed with exit 0:

```text
python -m unittest discover -v
Ran 52 tests
OK

python -m review.test_publication
Ran 10 tests
OK
```

`py_compile` and `git diff --check` also completed with exit 0. An isolated `jsonschema[format]` Draft 2020-12 oracle executed 19 differential cases with zero mismatches. The 24-input conformance/example matrix retained zero expectation mismatches, and six JSON CLI cases had zero exit-code, payload, or `world_truth` mismatches. Disclosure scanning found no forbidden private paths, share links, private vocabulary, Cyrillic text, or secret-shaped values; the only GitHub owner found was the required public owner in pinned source coordinates.

Trivy 0.72.0 completed with exit 0 using `vuln,misconfig,secret`, HIGH/CRITICAL, and `--ignore-unfixed`. The secret scanner reported no issues. No supported language manifest or configuration target existed for the vulnerability and misconfiguration scanners, so their result is recorded as not scanned rather than clean.

## Late full-audit reconciliation

The complete saved async review artifact arrived after the preliminary post-audit gate. Its `FAILED` verdict against old tree `5d68694c8358badd7384a5a0bdc7dbf13be8d119` contained six P1 and three P2 findings. The preliminary readiness statement and post-fix tree `df2b29eff18e0dec17ccd52eea1ab284fbef671d` were therefore superseded as release authorization.

Eight findings were already closed by the preceding correction pass: addressable locations; expected-record, external-producer, free-text, and previous-digest scope wording; public source-owner policy; malformed supported schema assertions; and failure-result `world_truth`. The full report additionally identified exponent-overflow JSON numbers. Both `1e400` and `-1e400` escaped strict parsing as host infinities.

A focused regression was run before implementation and failed twice because `ParseFailure` was not raised. The parser now uses a finite-checking `parse_float` hook. Re-running the focused test passed for both signs. Because this production change invalidated all earlier GREEN evidence, the complete suite, independent oracle, CLI matrix, disclosure scan, security scan, staged-tree fingerprint, and independent follow-up must be rerun on a new tree before commit.

The post-overflow complete gate then passed:

```text
python -m unittest discover -v
Ran 53 tests
OK

python -m review.test_publication
Ran 10 tests
OK
```

The isolated oracle retained 19 differential schema cases, 24 corpus/example inputs, and six standard CLI cases with zero mismatches; its two explicit overflow parser probes also had zero mismatches. A process-level known-valid trace mutated to `trace_revision: 1e400` returned exit 2, `INVALID`, `PARSE_FAILURE`, and `world_truth: NOT_EVALUATED`. The disposable trace was removed after execution.

## Focused follow-up closure

The independent follow-up against tree `c91bd0add4f95b72a66eb022e368b6b11815764a` reran 53 checked-in tests, 10 publication tests, 24 fixture/example CLI processes, 6 standard CLI cases, 19 Draft 2020-12 instance-parity mutations, and 61 focused probes. Eight prior findings were closed, but the reviewer correctly returned `VERDICT: FAILED`: 1 of 17 supported-keyword schema mutations remained fail-open. `type: ["integer", "integer"]` was accepted although the Draft 2020-12 metaschema requires unique array members.

A ninth malformed-keyword mutation was added before implementation and failed because `SchemaFailure` was not raised. The schema preflight now rejects duplicate type names after validating their supported string values. The focused regression then passed. All GREEN evidence for `c91bd0a...` is superseded; a new staged tree and complete gate are required.

The post-fix complete gate passed 53 checked-in tests and 10 publication tests, plus `py_compile` and `git diff --check`. A disposable `hermes-verify-*` script independently checked the exact duplicate-type mutation: the CDTS loader returned controlled `SchemaFailure`, Draft 2020-12 `check_schema` returned `SchemaError`, and the unchanged canonical schema passed its metaschema. The verifier was removed after execution.

## Publication status transition

Immediately before first public publication, a publication regression required README to identify the artifact as an `exploratory public draft` and reject stale `unpublished candidate` wording. The focused test failed against the audited local candidate, then passed after changing only README status wording and removing the contradictory no-publication sentence. The multi-implementation conformance disclaimer remains unchanged in substance. This publication-only delta requires a fresh complete local gate before push.
