"""Behavior tests for the corrected CDTS v0.1 boundary.

These tests implement review/ARCHITECTURAL_CORRECTION_GATE.md. They supersede
proposal-level assumptions from the original handoff.
"""
from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from validator.cdts_validate import ParseFailure, SchemaFailure, main, validate_data, validate_file

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "MPAA": ("https://github.com/gv1983us-commits/mpaa", "0d1aaf35cc4826622f3312fdd2a1c2d40890b965", "normative_source"),
    "BEC": ("https://github.com/gv1983us-commits/behavioral-execution-contract", "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261", "normative_source"),
    "PCA": ("https://github.com/gv1983us-commits/pca", "a669f023198615ad929f42df84f19380b57ca5ea", "normative_source"),
    "REVIEW_PROTOCOL": ("https://github.com/gv1983us-commits/repository-canon-review-protocol", "b4205ffd91a6316ab40243cbf8161a1c512cae1f", "source_policy"),
    "ARB": ("https://github.com/gv1983us-commits/agent-runtime-boundaries", "bcf9f628ee1d7c2075673b00f660674680bb6f62", "analytical_mapping"),
}


def source(owner: str) -> dict:
    repository, revision, role = PINS[owner]
    return {"owner": owner, "repository": repository, "revision": revision, "role": role}


def record_ref(ref_id: str, owner: str, record_type: str, record_id: str, minute: int) -> dict:
    return {
        "ref_id": ref_id,
        "owner": owner,
        "specification_revision": PINS[owner][1],
        "record_type": record_type,
        "record_id": record_id,
        "location": f"https://records.example.invalid/{owner.lower()}/{record_id}",
        "digest": "sha256:" + ("a" * 64),
        "recorded_at": f"2026-01-01T00:{minute:02d}:00Z",
        "link_direction": "external_to_cdts",
        "non_import_boundary": "trace_reference_only",
        "conclusion_imported": False,
    }


def base_trace() -> dict:
    return {
        "cdts_version": "0.1",
        "trace_id": "cdts-test-001",
        "trace_revision": 1,
        "trace_scope": {
            "scope_id": "scope-test-001",
            "correlation_subject": "municipal-notification-operation",
            "summary": "Records correlated around a bounded infrastructure operation.",
            "observed_from": "2026-01-01T00:00:00Z",
            "observed_to": "2026-01-01T00:10:00Z",
            "scope_status": "correlation_scope",
        },
        "source_revisions": [source("MPAA"), source("BEC"), source("REVIEW_PROTOCOL")],
        "record_refs": [
            record_ref("ref-mpaa-1", "MPAA", "runtime_report", "owner-local-1", 4),
            record_ref("ref-bec-1", "BEC", "execution_record", "owner-local-1", 5),
        ],
        "absences": [{
            "absence_id": "absence-pca-1",
            "owner": "PCA",
            "record_type": "transition_record",
            "state": "not_applicable",
            "reason": "No process-continuity claim is in this correlation scope.",
        }],
        "linkage_assertions": [{
            "linkage_id": "link-1",
            "from_ref": "ref-mpaa-1",
            "to_ref": "ref-bec-1",
            "relationship": "cdts.correlates",
            "direction": "undirected",
            "basis": "cdts.explicit_reference",
            "evidence_refs": [],
            "assertion_status": "cdts.declared",
            "asserted_by": "urn:example:producer:trace-builder",
            "asserted_at": "2026-01-01T00:11:00Z",
        }],
        "conflicts": [],
        "unresolved": [],
        "provenance": {
            "produced_by": "urn:example:producer:trace-builder",
            "produced_at": "2026-01-01T00:12:00Z",
            "producer_role": "coordination_layer",
            "notes": [],
        },
        "amendments": [],
    }


class StrictParsingTests(unittest.TestCase):
    def _write(self, payload: bytes) -> Path:
        handle = tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False)
        handle.write(payload); handle.close(); path = Path(handle.name)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_duplicate_keys_are_rejected(self):
        with self.assertRaises(ParseFailure):
            validate_file(self._write(b'{"cdts_version":"0.1","cdts_version":"0.1"}'))

    def test_nonfinite_numbers_are_rejected(self):
        for token in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(token=token), self.assertRaises(ParseFailure):
                validate_file(self._write(b'{"value":' + token + b'}'))

    def test_exponent_overflow_is_rejected_during_parsing(self):
        for token in (b"1e400", b"-1e400"):
            with self.subTest(token=token), self.assertRaises(ParseFailure):
                validate_file(self._write(b'{"value":' + token + b'}'))

    def test_invalid_utf8_is_rejected(self):
        with self.assertRaises(ParseFailure):
            validate_file(self._write(b"\xff"))

    def test_cli_parse_failure_reports_world_truth(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--json", str(self._write(b'{"x":1,"x":2}'))])
        payload = json.loads(output.getvalue())
        self.assertEqual(2, code)
        self.assertEqual("NOT_EVALUATED", payload["world_truth"])

    def test_cli_schema_failure_reports_world_truth(self):
        output = io.StringIO()
        with mock.patch("validator.cdts_validate.validate_file", side_effect=SchemaFailure("broken schema")):
            with redirect_stdout(output):
                code = main(["--json", str(self._write(b"{}"))])
        payload = json.loads(output.getvalue())
        self.assertEqual(2, code)
        self.assertEqual("TOOL_FAILURE", payload["status"])
        self.assertEqual("NOT_EVALUATED", payload["world_truth"])


class BoundaryTests(unittest.TestCase):
    def assert_invalid(self, trace: dict, code: str):
        result = validate_data(trace)
        self.assertEqual("INVALID", result.status, result.errors)
        self.assertIn(code, [error.code for error in result.errors], result.errors)

    def test_minimal_trace_is_admissible_and_world_truth_not_evaluated(self):
        result = validate_data(base_trace())
        self.assertEqual("ADMISSIBLE", result.status, result.errors)
        self.assertEqual("NOT_EVALUATED", result.world_truth)

    def test_producer_authored_validation_is_rejected(self):
        trace = base_trace(); trace["validation"] = {"admissibility": "PASS"}
        self.assert_invalid(trace, "SCHEMA_ADDITIONAL_PROPERTY")

    def test_event_identity_surface_is_rejected(self):
        trace = base_trace(); trace["event"] = trace.pop("trace_scope")
        self.assert_invalid(trace, "SCHEMA_REQUIRED")

    def test_integer_valued_json_number_matches_dialect(self):
        trace = base_trace(); trace["trace_revision"] = 1.0
        self.assertEqual("ADMISSIBLE", validate_data(trace).status)

    def test_non_json_in_memory_value_fails_closed(self):
        trace = base_trace(); trace["linkage_assertions"][0]["evidence_refs"] = [set()]
        self.assert_invalid(trace, "SCHEMA_TYPE")

    def test_missing_required_field_is_rejected(self):
        trace = base_trace(); del trace["trace_scope"]["summary"]
        self.assert_invalid(trace, "SCHEMA_REQUIRED")

    def test_unknown_version_and_property_fail_closed(self):
        trace = base_trace(); trace["cdts_version"] = "0.2"
        self.assert_invalid(trace, "SCHEMA_CONST")
        trace = base_trace(); trace["domain_verdict"] = "FULL-for-task"
        self.assert_invalid(trace, "SCHEMA_ADDITIONAL_PROPERTY")

    def test_owner_local_record_ids_need_not_be_globally_unique(self):
        trace = base_trace()
        self.assertEqual(trace["record_refs"][0]["record_id"], trace["record_refs"][1]["record_id"])
        self.assertEqual("ADMISSIBLE", validate_data(trace).status)

    def test_local_ref_ids_are_unique(self):
        trace = base_trace(); trace["record_refs"][1]["ref_id"] = "ref-mpaa-1"
        self.assert_invalid(trace, "DUPLICATE_ID")

    def test_external_reference_is_fully_qualified(self):
        for field in ("owner", "specification_revision", "record_type", "record_id", "location", "digest", "link_direction", "non_import_boundary", "conclusion_imported"):
            with self.subTest(field=field):
                trace = base_trace(); del trace["record_refs"][0][field]
                self.assert_invalid(trace, "SCHEMA_REQUIRED")

    def test_external_location_is_addressable(self):
        trace = base_trace(); trace["record_refs"][0]["location"] = "x"
        self.assert_invalid(trace, "SCHEMA_PATTERN")

    def test_bad_digest_and_pin_are_rejected(self):
        trace = base_trace(); trace["record_refs"][0]["digest"] = "sha256:no"
        self.assert_invalid(trace, "SCHEMA_PATTERN")
        trace = base_trace(); trace["record_refs"][0]["specification_revision"] = "f" * 40
        self.assert_invalid(trace, "REFERENCE_PIN_MISMATCH")

    def test_import_boundary_is_not_negotiable(self):
        trace = base_trace(); trace["record_refs"][0]["conclusion_imported"] = True
        self.assert_invalid(trace, "SCHEMA_CONST")
        trace = base_trace(); trace["record_refs"][0]["conclusion_imported"] = 0
        self.assert_invalid(trace, "SCHEMA_CONST")
        trace = base_trace(); trace["record_refs"][0]["non_import_boundary"] = "interpret_and_compare"
        self.assert_invalid(trace, "SCHEMA_CONST")

    def test_native_or_cross_domain_conclusions_cannot_be_embedded(self):
        for field in ("claims", "conclusion", "deployment_level", "overall_status", "task_result"):
            with self.subTest(field=field):
                trace = base_trace(); trace["record_refs"][0][field] = "FULL"
                self.assert_invalid(trace, "SCHEMA_ADDITIONAL_PROPERTY")

    def test_pca_v01_linkage_record_is_not_a_current_record_type(self):
        trace = base_trace(); trace["source_revisions"].append(source("PCA"))
        trace["record_refs"].append(record_ref("ref-pca-old", "PCA", "linkage_record", "legacy-link-1", 6))
        self.assert_invalid(trace, "PCA_LINKAGE_SUPERSEDED")

    def test_arb_is_analytical_and_review_protocol_is_policy_only(self):
        trace = base_trace(); arb = source("ARB"); arb["role"] = "normative_source"; trace["source_revisions"].append(arb)
        self.assert_invalid(trace, "SOURCE_ROLE_MISMATCH")
        trace = base_trace(); trace["source_revisions"][2]["role"] = "normative_source"
        self.assert_invalid(trace, "SOURCE_ROLE_MISMATCH")

    def test_missing_or_wrong_source_pin_is_rejected(self):
        trace = base_trace(); trace["source_revisions"] = [item for item in trace["source_revisions"] if item["owner"] != "BEC"]
        self.assert_invalid(trace, "SOURCE_PIN_REQUIRED")
        trace = base_trace(); trace["source_revisions"][0]["revision"] = "f" * 40
        self.assert_invalid(trace, "SOURCE_PIN_MISMATCH")

    def test_link_endpoints_resolve_by_local_ref_and_self_links_fail(self):
        trace = base_trace(); trace["linkage_assertions"][0]["to_ref"] = "missing"
        self.assert_invalid(trace, "DANGLING_REFERENCE")
        trace = base_trace(); trace["linkage_assertions"][0]["to_ref"] = "ref-mpaa-1"
        self.assert_invalid(trace, "SELF_LINK")

    def test_vocabulary_is_namespaced_and_causality_is_not_in_v01(self):
        for value in ("OBSERVED", "DESCRIBES_SAME_EVENT", "TRIGGERED_BY", "CONTRIBUTED_TO", "REQUIRED_FOR", "cdts.triggered_by"):
            with self.subTest(value=value):
                trace = base_trace(); trace["linkage_assertions"][0]["relationship"] = value
                self.assert_invalid(trace, "SCHEMA_ENUM")

    def test_precedes_must_match_record_timestamps(self):
        trace = base_trace(); link = trace["linkage_assertions"][0]
        link.update({"from_ref": "ref-bec-1", "to_ref": "ref-mpaa-1", "relationship": "cdts.precedes", "direction": "directed", "basis": "cdts.timestamp_order", "assertion_status": "cdts.derived"})
        self.assert_invalid(trace, "TEMPORAL_ORDER")

    def test_scope_and_provenance_time_are_ordered(self):
        trace = base_trace(); trace["trace_scope"]["observed_from"] = "20260101T000000Z"
        self.assert_invalid(trace, "SCHEMA_PATTERN")
        trace = base_trace(); trace["trace_scope"]["observed_from"] = "2026-01-01T00:00:00+00:00"
        self.assert_invalid(trace, "SCHEMA_PATTERN")
        trace = base_trace(); trace["trace_scope"]["observed_from"] = "2026-01-01T00:20:00Z"
        self.assert_invalid(trace, "SCOPE_INTERVAL")
        trace = base_trace(); trace["provenance"]["produced_at"] = "2025-12-31T23:59:00Z"
        self.assert_invalid(trace, "PROVENANCE_TIME")

    def test_trace_producer_is_qualified(self):
        trace = base_trace(); trace["provenance"]["produced_by"] = "MPAA"
        self.assert_invalid(trace, "SCHEMA_PATTERN")

    def test_typed_absence_is_distinct_from_unresolved(self):
        trace = base_trace(); trace["absences"][0] = None
        self.assert_invalid(trace, "SCHEMA_TYPE")
        trace = base_trace(); trace["absences"][0]["state"] = "UNKNOWN"
        self.assert_invalid(trace, "SCHEMA_ENUM")

    def test_disclosed_conflict_is_admissible_without_selecting_winner(self):
        trace = base_trace(); trace["conflicts"] = [{
            "conflict_id": "conflict-1",
            "record_refs": ["ref-mpaa-1", "ref-bec-1"],
            "native_claim_pointer": "external_effect_observed",
            "positions": [
                {"record_ref": "ref-mpaa-1", "position_digest": "sha256:" + "b" * 64},
                {"record_ref": "ref-bec-1", "position_digest": "sha256:" + "c" * 64},
            ],
            "resolution": "unresolved",
            "precedence_policy_ref": None,
        }]
        result = validate_data(trace)
        self.assertEqual("ADMISSIBLE_WITH_CONFLICTS", result.status, result.errors)

    def test_conflict_positions_match_declared_records_exactly(self):
        trace = base_trace(); trace["conflicts"] = [{
            "conflict_id": "conflict-1",
            "record_refs": ["ref-mpaa-1", "ref-bec-1"],
            "native_claim_pointer": "external_effect_observed",
            "positions": [
                {"record_ref": "ref-mpaa-1", "position_digest": "sha256:" + "b" * 64},
                {"record_ref": "ref-mpaa-1", "position_digest": "sha256:" + "c" * 64},
            ],
            "resolution": "unresolved",
            "precedence_policy_ref": None,
        }]
        self.assert_invalid(trace, "CONFLICT_POSITION_MISMATCH")

    def test_conflict_winner_requires_external_policy_and_remains_disclosed(self):
        trace = base_trace(); trace["conflicts"] = [{
            "conflict_id": "conflict-1", "record_refs": ["ref-mpaa-1", "ref-bec-1"],
            "native_claim_pointer": "external_effect_observed",
            "positions": [{"record_ref": "ref-mpaa-1", "position_digest": "sha256:" + "b" * 64}, {"record_ref": "ref-bec-1", "position_digest": "sha256:" + "c" * 64}],
            "resolution": "selected_for_local_decision", "precedence_policy_ref": None,
        }]
        self.assert_invalid(trace, "CONFLICT_POLICY_REQUIRED")
        trace["conflicts"][0]["precedence_policy_ref"] = "x"
        self.assert_invalid(trace, "SCHEMA_PATTERN")
        trace["conflicts"][0]["precedence_policy_ref"] = "https://policy.example.invalid/conflict-precedence/v1"
        self.assertEqual("ADMISSIBLE_WITH_CONFLICTS", validate_data(trace).status)

    def test_complete_unresolved_is_admissible_and_dangling_link_is_not(self):
        trace = base_trace(); trace["unresolved"] = [{
            "unresolved_id": "unresolved-1", "question": "Do these records share one correlation scope?",
            "status": "open", "required_evidence": ["An addressable correlation receipt"],
            "linkage_refs": ["link-1"],
        }]
        self.assertEqual("ADMISSIBLE_WITH_UNRESOLVED", validate_data(trace).status)
        trace["unresolved"][0]["linkage_refs"] = ["missing"]
        self.assert_invalid(trace, "DANGLING_REFERENCE")

    def test_amendment_chain_is_contiguous_and_required_after_revision_one(self):
        trace = base_trace(); trace["trace_revision"] = 2
        self.assert_invalid(trace, "AMENDMENT_REQUIRED")
        trace["amendments"] = [{
            "from_revision": 1, "to_revision": 2,
            "previous_trace_digest": "sha256:" + "d" * 64,
            "amended_at": "2026-01-01T00:13:00Z",
            "reason": "Added an independently addressable reference.",
            "changed_fields": ["/record_refs"],
        }]
        self.assertEqual("ADMISSIBLE", validate_data(trace).status)


class CorpusTests(unittest.TestCase):
    def test_fixture_expectations(self):
        for path in sorted((ROOT / "conformance" / "fixtures").glob("*.json")):
            with self.subTest(path=path.name):
                if "malformed" in path.name:
                    with self.assertRaises(ParseFailure): validate_file(path)
                else:
                    result = validate_file(path)
                    expected_valid = path.name.startswith("valid-")
                    self.assertEqual(expected_valid, result.status != "INVALID", result.errors)

    def test_examples_are_admissible(self):
        for path in sorted((ROOT / "examples").glob("*.json")):
            with self.subTest(path=path.name):
                self.assertNotEqual("INVALID", validate_file(path).status)


if __name__ == "__main__":
    unittest.main()
