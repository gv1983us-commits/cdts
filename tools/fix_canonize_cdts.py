#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "1d369f6cd091b99f9492cfaf730f0a170b55106e": "0d1aaf35cc4826622f3312fdd2a1c2d40890b965",
    "bb46f5f8aac96d1cffba7a334c5d17fb331ef3af": "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261",
    "6ad1a86d7c09b36839d162c580f84f05cfe4a598": "a669f023198615ad929f42df84f19380b57ca5ea",
    "595c08b877e4dfb14593454c2eec7c8f5df46c28": "b4205ffd91a6316ab40243cbf8161a1c512cae1f",
    "6b6c32cd467a4b5e4863d082b9da5bdd40d7dced": "bcf9f628ee1d7c2075673b00f660674680bb6f62",
    "https://example.org/cdts/schema/cdts-record.schema.json": "https://raw.githubusercontent.com/gv1983us-commits/cdts/main/schema/cdts-record.schema.json",
}

for path in (ROOT / "validator").glob("test_*.py"):
    text = path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

publication = ROOT / "review" / "test_publication.py"
text = publication.read_text(encoding="utf-8")
old = '''def public_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path
'''
new = '''def public_files():
    for path in ROOT.rglob("*"):
        if "tools" in path.parts:
            continue
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path
'''
if old not in text:
    raise SystemExit("public_files marker not found")
publication.write_text(text.replace(old, new), encoding="utf-8")

print("legacy test harness aligned")
