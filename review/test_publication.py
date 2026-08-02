"""Pre-publication boundary checks for the local CDTS candidate."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from validator.cdts_validate import PINNED_SOURCES, ParseFailure, parse_json_bytes, validate_file

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "LICENSE", "spec/00_CDTS_IN_60_SECONDS.md", "spec/01_CDTS_CORE.md",
    "spec/02_RELATIONSHIP_VOCABULARY.md", "spec/03_SOURCE_REVISION_POLICY.md", "spec/04_CONFORMANCE.md",
    "schema/cdts-record.schema.json", "validator/cdts_validate.py", "validator/README.md",
    "validator/test_validator.py", "validator/test_schema_parity.py", "conformance/README.md",
    "conformance/RESISTANCE_CORPUS.md", "examples/mpaa-bec-execution.json",
    "examples/mpaa-pca-host-transition.json", "examples/full-cross-domain-event.json",
    "references/PINNED_SPEC_REVISIONS.md", "review/TDD_LOG.md", ".github/workflows/ci.yml", ".gitignore",
}
PUBLIC_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}


def public_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path


class PublicationTests(unittest.TestCase):
    def test_required_artifacts_exist(self):
        missing = sorted(name for name in REQUIRED if not (ROOT / name).is_file())
        self.assertEqual([], missing)

    def test_readme_declares_public_draft_status(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("exploratory public draft", readme)
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

    def test_no_local_paths_or_private_share_links(self):
        slash = "/"
        backslash = "\\"
        forbidden = (
            "C:" + backslash + "Users" + backslash,
            slash + "Users" + slash,
            slash + "home" + slash,
            "chatgpt.com" + slash + "share" + slash,
            "localhost" + ":",
        )
        for path in public_files():
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(path=path.relative_to(ROOT), token=token):
                    self.assertNotIn(token, text)

    def test_public_surface_is_ascii(self):
        for path in public_files():
            if path.name.startswith("test_") or path.name == "cdts_validate.py":
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(re.search(r"[^\x00-\x7f]", text))

    def test_no_producer_authored_validation_surface(self):
        schema = json.loads((ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("validation", schema["properties"])
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "conformance" / "fixtures").glob("valid-*.json")):
            self.assertNotIn("validation", json.loads(path.read_text(encoding="utf-8")))

    def test_v01_schema_has_no_causal_relationship_tokens(self):
        schema_text = (ROOT / "schema" / "cdts-record.schema.json").read_text(encoding="utf-8").lower()
        for token in ("triggered_by", "contributed_to", "required_for"):
            self.assertNotIn(token, schema_text)

    def test_pins_are_documented(self):
        text = (ROOT / "references" / "PINNED_SPEC_REVISIONS.md").read_text(encoding="utf-8")
        for _, revision, _ in PINNED_SOURCES.values():
            self.assertIn(revision, text)

    def test_normative_boundaries_match_machine_surface(self):
        core = (ROOT / "spec" / "01_CDTS_CORE.md").read_text(encoding="utf-8")
        conformance = (ROOT / "spec" / "04_CONFORMANCE.md").read_text(encoding="utf-8")
        gate = (ROOT / "review" / "ARCHITECTURAL_CORRECTION_GATE.md").read_text(encoding="utf-8")
        self.assertIn("does not define an expected-record universe", core)
        self.assertIn("External record producer identity and distinctness are `NOT_EVALUATED`", core)
        self.assertIn("previous-digest correspondence is `NOT_EVALUATED`", core)
        self.assertIn("does not semantically classify free-text values", core)
        self.assertIn("does not semantically classify free-text values", conformance)
        self.assertIn("Public source coordinates MAY include", gate)

    def test_github_actions_are_pinned_by_commit(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        uses = re.findall(r"^\s*(?:-\s+)?uses:\s+([^\s#]+)", workflow, flags=re.MULTILINE)
        self.assertGreater(len(uses), 0)
        for action in uses:
            with self.subTest(action=action):
                self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
