"""Publication and boundary checks for the canonical CDTS artifact."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from validator.cdts_validate import PINNED_SOURCES, parse_json_bytes, validate_file

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "CANON.md", "ARTIFACT.json", "RELATIONS.md", "PROVENANCE.md", "LICENSE",
    "spec/00_CDTS_IN_60_SECONDS.md", "spec/01_CDTS_CORE.md",
    "spec/02_RELATIONSHIP_VOCABULARY.md", "spec/03_SOURCE_REVISION_POLICY.md",
    "spec/04_CONFORMANCE.md", "schema/cdts-record.schema.json",
    "validator/cdts_validate.py", "validator/README.md", "validator/test_validator.py",
    "validator/test_schema_parity.py", "validator/test_external_evaluation_trace.py",
    "conformance/README.md", "conformance/RESISTANCE_CORPUS.md",
    "examples/mpaa-bec-execution.json", "examples/mpaa-pca-host-transition.json",
    "examples/full-cross-domain-event.json", "examples/external-evaluation-run.json",
    "references/PINNED_SPEC_REVISIONS.md", "review/TDD_LOG.md",
    "review/ARCHITECTURAL_CORRECTION_GATE.md", "review/PUBLICATION_MANIFEST.md",
    "review/2026-08-06_CANONIZATION_REVIEW.md", "review/test_artifact_canon.py",
    ".github/workflows/ci.yml", ".gitignore",
}
PUBLIC_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}
EXPECTED_PINS = {
    "MPAA": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "BEC": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "PCA": "a669f023198615ad929f42df84f19380b57ca5ea",
    "REVIEW_PROTOCOL": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "ARB": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
}


def public_files():
    for path in ROOT.rglob("*"):
        if "tools" in path.parts:
            continue
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path


class PublicationTests(unittest.TestCase):
    def test_required_artifacts_exist(self):
        self.assertEqual([], sorted(name for name in REQUIRED if not (ROOT / name).is_file()))

    def test_readme_declares_canonical_public(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("canonical_public", readme)
        self.assertIn("Artifact version", readme)
        self.assertIn("Record profile", readme)
        self.assertNotIn("unpublished candidate", readme)

    def test_all_machine_json_is_strict(self):
        for path in ROOT.rglob("*.json"):
            if "malformed-" in path.name:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                parse_json_bytes(path.read_bytes())

    def test_examples_and_positive_fixtures_are_admissible(self):
        paths = list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("valid-*.json"))
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotEqual("INVALID", validate_file(path).status)

    def test_current_pins_are_consistent_everywhere_active(self):
        self.assertEqual({owner: value[1] for owner, value in PINNED_SOURCES.items()}, EXPECTED_PINS)
        receipt = (ROOT / "references" / "PINNED_SPEC_REVISIONS.md").read_text(encoding="utf-8")
        for owner, revision in EXPECTED_PINS.items():
            self.assertIn(revision, receipt, owner)
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("*.json")):
            if path.name.startswith("malformed-"):
                continue
            text = path.read_text(encoding="utf-8")
            for old in (
                "1d369f6cd091b99f9492cfaf730f0a170b55106e",
                "bb46f5f8aac96d1cffba7a334c5d17fb331ef3af",
                "6ad1a86d7c09b36839d162c580f84f05cfe4a598",
                "595c08b877e4dfb14593454c2eec7c8f5df46c28",
                "6b6c32cd467a4b5e4863d082b9da5bdd40d7dced",
            ):
                self.assertNotIn(old, text, str(path.relative_to(ROOT)))

    def test_no_local_paths_private_links_or_credentials(self):
        forbidden = re.compile(
            r"(C:\\Users\\|/Users/|/home/|chatgpt\.com/share/|localhost:|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|ghp_[A-Za-z0-9]+|"
            r"github_pat_[A-Za-z0-9_]+|(?<![A-Za-z0-9])sk-[A-Za-z0-9]+)",
            re.IGNORECASE,
        )
        for path in public_files():
            if path.resolve() == Path(__file__).resolve():
                continue
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), str(path.relative_to(ROOT)))

    def test_public_surface_is_ascii(self):
        for path in public_files():
            if path.name.startswith("test_") or path.name == "cdts_validate.py":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[^\x00-\x7f]", text), str(path.relative_to(ROOT)))

    def test_no_producer_authored_validation_surface(self):
        schema = json.loads((ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("validation", schema["properties"])
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("valid-*.json")):
            self.assertNotIn("validation", json.loads(path.read_text(encoding="utf-8")))

    def test_profile_v01_has_no_causal_relationship_tokens(self):
        schema_text = (ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8").lower()
        for token in ("triggered_by", "contributed_to", "required_for"):
            self.assertNotIn(token, schema_text)

    def test_normative_boundaries_match_machine_surface(self):
        artifact = json.loads((ROOT / "ARTIFACT.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["normative_surface_count"], 5)
        self.assertFalse(artifact["reference_implementation"]["normative"])
        self.assertTrue(all(value is False for value in artifact["assertion_boundaries"].values()))

    def test_github_actions_are_pinned_by_commit(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        uses = re.findall(r"^\s*(?:-\s+)?uses:\s+([^\s#]+)", workflow, flags=re.MULTILINE)
        self.assertGreater(len(uses), 0)
        for action in uses:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_license_is_declared_and_present(self):
        artifact = json.loads((ROOT / "ARTIFACT.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["license"], "MIT")
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
