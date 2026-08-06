from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "ARTIFACT.json"
CANON = ROOT / "CANON.md"
RELATIONS = ROOT / "RELATIONS.md"
PROVENANCE = ROOT / "PROVENANCE.md"
RECEIPT = ROOT / "references" / "PINNED_SPEC_REVISIONS.md"

EXPECTED_SURFACES = {
    "spec/01_CDTS_CORE.md",
    "spec/02_RELATIONSHIP_VOCABULARY.md",
    "spec/03_SOURCE_REVISION_POLICY.md",
    "spec/04_CONFORMANCE.md",
    "schema/cdts-record.schema.json",
}
EXPECTED_RELATIONS = {
    "claude.bec": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "claude.mpaa": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "claude.pca": "a669f023198615ad929f42df84f19380b57ca5ea",
    "claude.review_protocol": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "claude.arb": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
}


class ArtifactCanonTests(unittest.TestCase):
    def artifact(self):
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_identity_and_versions(self):
        artifact = self.artifact()
        self.assertEqual(artifact["artifact_id"], "claude.cdts")
        self.assertEqual(artifact["repository"], "gv1983us-commits/cdts")
        self.assertEqual(artifact["artifact_version"], "0.2-draft")
        self.assertEqual(artifact["record_profile_version"], "0.1-draft")
        self.assertEqual(artifact["artifact_status"], "canonical_public_draft")
        self.assertEqual(artifact["license"], "MIT")

    def test_five_surface_authority_matrix(self):
        artifact = self.artifact()
        self.assertEqual(artifact["normative_authority_model"], "five_surface_domain_ownership_matrix")
        self.assertEqual(artifact["normative_surface_count"], 5)
        self.assertEqual({item["path"] for item in artifact["normative_surfaces"]}, EXPECTED_SURFACES)
        self.assertFalse(artifact["reference_implementation"]["normative"])
        self.assertNotIn("references/PINNED_SPEC_REVISIONS.md", EXPECTED_SURFACES)

    def test_five_relations_are_exact_and_non_importing(self):
        relations = {item["artifact_id"]: item for item in self.artifact()["relations"]}
        self.assertEqual(set(relations), set(EXPECTED_RELATIONS))
        for artifact_id, revision in EXPECTED_RELATIONS.items():
            with self.subTest(artifact_id=artifact_id):
                self.assertEqual(relations[artifact_id]["reviewed_revision"], revision)
                self.assertFalse(relations[artifact_id]["conclusion_imported"])

    def test_all_assertion_boundaries_remain_false(self):
        boundaries = self.artifact()["assertion_boundaries"]
        self.assertTrue(boundaries)
        self.assertTrue(all(value is False for value in boundaries.values()))

    def test_human_surfaces_publish_core_boundaries(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (CANON, RELATIONS, PROVENANCE, RECEIPT)
        )
        for marker in (
            "normative_surface_count = 5",
            "not a sixth",
            "conclusion_imported: false",
            "correlation != event identity",
            "sequence != causality",
            "world truth",
            "reciprocal",
        ):
            self.assertIn(marker.lower(), combined.lower())

    def test_schema_identity_is_repository_owned(self):
        schema = json.loads((ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            schema["$id"],
            "https://raw.githubusercontent.com/gv1983us-commits/cdts/main/schema/cdts-record.schema.json",
        )
        self.assertEqual(schema["properties"]["cdts_version"]["const"], "0.1-draft")


if __name__ == "__main__":
    unittest.main()
