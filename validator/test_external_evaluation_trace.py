"""Regression tests for the CDTS external-evaluation trace profile."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validator.cdts_validate import validate_data

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "external-evaluation-run.json"


def load_trace() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


class ExternalEvaluationTraceTests(unittest.TestCase):
    def test_example_is_admissible_with_unresolved_and_no_world_truth(self):
        trace = load_trace()
        result = validate_data(trace)

        self.assertEqual(result.status, "ADMISSIBLE_WITH_UNRESOLVED", result.errors)
        self.assertEqual(result.world_truth, "NOT_EVALUATED")
        self.assertEqual(len(trace["record_refs"]), 2)
        self.assertEqual({ref["owner"] for ref in trace["record_refs"]}, {"MPAA", "BEC"})
        self.assertTrue(all(ref["conclusion_imported"] is False for ref in trace["record_refs"]))

    def test_donor_digest_is_scope_key_not_record_owner(self):
        trace = load_trace()
        summary = trace["trace_scope"]["summary"]
        self.assertIn("sha256:" + "a" * 64, summary)
        self.assertIn("does not prove donor authenticity", summary)
        self.assertNotIn("JARVIS_OS", {ref["owner"] for ref in trace["record_refs"]})

    def test_trace_explicitly_distinguishes_evaluation_from_implementation(self):
        notes = "\n".join(load_trace()["provenance"]["notes"])
        self.assertIn("independent evaluation of one implementation", notes)
        self.assertIn("not an independent implementation", notes)

    def test_redaction_and_evaluator_provenance_remain_unresolved(self):
        trace = load_trace()
        unresolved = {item["unresolved_id"]: item for item in trace["unresolved"]}
        self.assertIn("unresolved-donor-redaction-001", unresolved)
        self.assertIn("unresolved-evaluator-provenance-001", unresolved)
        self.assertIn("review receipt", unresolved["unresolved-donor-redaction-001"]["required_evidence"][0])

    def test_importing_domain_verdict_is_rejected(self):
        trace = copy.deepcopy(load_trace())
        trace["record_refs"][0]["task_result"] = "FULL"
        result = validate_data(trace)
        self.assertEqual(result.status, "INVALID")
        self.assertIn("SCHEMA_ADDITIONAL_PROPERTY", {error.code for error in result.errors})

    def test_claiming_causality_is_rejected(self):
        trace = copy.deepcopy(load_trace())
        link = trace["linkage_assertions"][0]
        link["relationship"] = "cdts.triggered_by"
        result = validate_data(trace)
        self.assertEqual(result.status, "INVALID")
        self.assertIn("SCHEMA_ENUM", {error.code for error in result.errors})

    def test_removing_unresolved_questions_does_not_create_certification(self):
        trace = copy.deepcopy(load_trace())
        trace["unresolved"] = []
        result = validate_data(trace)
        self.assertEqual(result.status, "ADMISSIBLE", result.errors)
        self.assertEqual(result.world_truth, "NOT_EVALUATED")
        notes = "\n".join(trace["provenance"]["notes"])
        self.assertIn("not a CDTS authenticity or redaction verdict", notes)


if __name__ == "__main__":
    unittest.main()
