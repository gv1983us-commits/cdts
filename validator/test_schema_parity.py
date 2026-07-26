"""Schema/validator parity tests for the corrected CDTS boundary."""
import copy
import unittest
from pathlib import Path

from validator.cdts_validate import (
    ABSENCE_STATES,
    ASSERTION_STATUSES,
    BASES,
    RELATIONSHIPS,
    SchemaFailure,
    load_schema,
    validate_data,
)
from validator.test_validator import base_trace

ROOT = Path(__file__).resolve().parents[1]


class SchemaParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_schema(ROOT / "schema" / "cdts-record.schema.json")
        cls.defs = cls.schema["$defs"]

    def test_schema_vocabulary_matches_validator(self):
        linkage = self.defs["linkageAssertion"]["properties"]
        self.assertEqual(set(RELATIONSHIPS), set(linkage["relationship"]["enum"]))
        self.assertEqual(set(ASSERTION_STATUSES), set(linkage["assertion_status"]["enum"]))
        self.assertEqual(set(BASES), set(linkage["basis"]["enum"]))
        self.assertEqual(set(ABSENCE_STATES), set(self.defs["absence"]["properties"]["state"]["enum"]))

    def test_v01_vocabulary_has_no_causal_relations(self):
        joined = " ".join(RELATIONSHIPS).lower()
        for token in ("trigger", "cause", "contributed", "required_for"):
            self.assertNotIn(token, joined)

    def test_schema_has_trace_scope_and_no_producer_validation(self):
        self.assertIn("trace_scope", self.schema["required"])
        self.assertNotIn("event", self.schema["properties"])
        self.assertNotIn("validation", self.schema["properties"])
        self.assertIn("record_refs", self.schema["required"])
        self.assertIn("linkage_assertions", self.schema["required"])

    def test_schema_rejects_unsupported_normative_keyword(self):
        schema = copy.deepcopy(self.schema); schema["allOf"] = []
        with self.assertRaises(SchemaFailure):
            load_schema(schema)

    def test_malformed_supported_keyword_values_fail_during_load(self):
        mutations = {
            "invalid pattern": lambda schema: schema["$defs"]["id"].__setitem__("pattern", "["),
            "noninteger minLength": lambda schema: schema["$defs"]["id"].__setitem__("minLength", "1"),
            "required is not an array": lambda schema: schema.__setitem__("required", "trace_id"),
            "properties is not an object": lambda schema: schema.__setitem__("properties", []),
            "oneOf is not an array": lambda schema: schema.__setitem__("oneOf", {}),
            "$ref is not a string": lambda schema: schema["properties"]["trace_id"].__setitem__("$ref", 3),
            "unknown type": lambda schema: schema["properties"]["trace_revision"].__setitem__("type", "imaginary"),
            "unsupported format": lambda schema: schema["$defs"]["timestamp"].__setitem__("format", "email"),
            "duplicate type": lambda schema: schema["properties"]["trace_revision"].__setitem__("type", ["integer", "integer"]),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                schema = copy.deepcopy(self.schema)
                mutate(schema)
                with self.assertRaises(SchemaFailure):
                    load_schema(schema)

    def test_schema_id_and_version_are_canonical(self):
        self.assertEqual("https://example.org/cdts/schema/cdts-record.schema.json", self.schema["$id"])
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", self.schema["$schema"])
        self.assertEqual("0.1-draft", self.schema["properties"]["cdts_version"]["const"])

    def test_each_required_root_property_is_enforced(self):
        for name in self.schema["required"]:
            with self.subTest(name=name):
                trace = base_trace(); del trace[name]
                self.assertEqual("INVALID", validate_data(trace).status)


if __name__ == "__main__":
    unittest.main()
