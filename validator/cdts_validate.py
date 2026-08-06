#!/usr/bin/env python
"""Dependency-free, fail-closed CDTS v0.1-draft reference validator."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

VERSION = "0.1-draft"
RELATIONSHIPS = (
    "cdts.references", "cdts.derived_from", "cdts.correlates", "cdts.has_external_reference",
    "cdts.has_transition_record", "cdts.has_execution_record", "cdts.precedes", "cdts.follows",
    "cdts.co_occurs_with", "cdts.overlaps", "cdts.temporal_order_undetermined",
    "cdts.does_not_imply", "cdts.conflicts_with", "cdts.partially_supports", "cdts.insufficient_for",
)
ASSERTION_STATUSES = ("cdts.observed", "cdts.declared", "cdts.derived", "cdts.hypothesis", "cdts.conflicting", "cdts.undetermined")
BASES = ("cdts.explicit_reference", "cdts.content_digest", "cdts.timestamp_order", "cdts.shared_receipt", "cdts.insufficient")
ABSENCE_STATES = ("not_applicable", "not_observed", "not_produced", "unavailable", "undetermined")
PINNED_SOURCES = {
    "MPAA": ("https://github.com/gv1983us-commits/mpaa", "0d1aaf35cc4826622f3312fdd2a1c2d40890b965", "normative_source"),
    "BEC": ("https://github.com/gv1983us-commits/behavioral-execution-contract", "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261", "normative_source"),
    "PCA": ("https://github.com/gv1983us-commits/pca", "a669f023198615ad929f42df84f19380b57ca5ea", "normative_source"),
    "REVIEW_PROTOCOL": ("https://github.com/gv1983us-commits/repository-canon-review-protocol", "b4205ffd91a6316ab40243cbf8161a1c512cae1f", "source_policy"),
    "ARB": ("https://github.com/gv1983us-commits/agent-runtime-boundaries", "bcf9f628ee1d7c2075673b00f660674680bb6f62", "analytical_mapping"),
}
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "cdts-record.schema.json"
SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "type", "const", "enum",
    "properties", "required", "additionalProperties", "items", "oneOf", "minItems", "maxItems",
    "uniqueItems", "minLength", "maxLength", "minimum", "maximum", "pattern", "format",
}


class ParseFailure(ValueError):
    """The input is not strict UTF-8 JSON."""


class SchemaFailure(RuntimeError):
    """The normative schema cannot be safely interpreted."""


@dataclass(frozen=True)
class ValidationError:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass(frozen=True)
class ValidationResult:
    status: str
    errors: tuple[ValidationError, ...]
    world_truth: str = "NOT_EVALUATED"

    @property
    def valid(self) -> bool:
        return self.status != "INVALID"

    def as_dict(self) -> dict[str, Any]:
        return {"status": self.status, "valid": self.valid, "world_truth": self.world_truth, "errors": [e.as_dict() for e in self.errors]}


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ParseFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ParseFailure(f"non-finite number is not permitted: {value}")


def _parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ParseFailure(f"non-finite number is not permitted: {value}")
    return parsed


def parse_json_bytes(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ParseFailure(f"input is not UTF-8: {exc}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=_reject_constant,
            parse_float=_parse_finite_float,
        )
    except ParseFailure:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ParseFailure(f"invalid JSON: {exc}") from exc


def _check_schema_keywords(schema: Any, path: str = "#", root: dict[str, Any] | None = None) -> None:
    if not isinstance(schema, dict):
        raise SchemaFailure(f"schema assertion at {path} must be an object")
    root = schema if root is None else root
    for key in schema:
        if key not in SUPPORTED_SCHEMA_KEYWORDS:
            raise SchemaFailure(f"unsupported normative schema keyword at {path}: {key}")

    for key in ("$schema", "$id", "$ref", "title", "description", "pattern", "format"):
        if key in schema and not isinstance(schema[key], str):
            raise SchemaFailure(f"schema keyword {key} at {path} must be a string")
    if "$ref" in schema:
        _resolve_ref(root, schema["$ref"])

    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        supported_types = {"object", "array", "string", "boolean", "integer", "number", "null"}
        if (
            not types
            or not all(isinstance(item, str) and item in supported_types for item in types)
            or len(types) != len(set(types))
        ):
            raise SchemaFailure(f"unsupported or malformed schema type at {path}: {expected!r}")

    for key in ("properties", "$defs"):
        if key in schema:
            values = schema[key]
            if not isinstance(values, dict):
                raise SchemaFailure(f"schema keyword {key} at {path} must be an object")
            for name, child in values.items():
                if not isinstance(name, str):
                    raise SchemaFailure(f"schema member name at {path}/{key} must be a string")
                _check_schema_keywords(child, f"{path}/{key}/{name}", root)

    if "required" in schema:
        required = schema["required"]
        if not isinstance(required, list) or not all(isinstance(item, str) for item in required) or len(required) != len(set(required)):
            raise SchemaFailure(f"schema keyword required at {path} must be an array of unique strings")

    if "additionalProperties" in schema:
        child = schema["additionalProperties"]
        if not isinstance(child, (bool, dict)):
            raise SchemaFailure(f"schema keyword additionalProperties at {path} must be boolean or object")
        if isinstance(child, dict):
            _check_schema_keywords(child, f"{path}/additionalProperties", root)

    if "items" in schema:
        child = schema["items"]
        if not isinstance(child, dict):
            raise SchemaFailure(f"schema keyword items at {path} must be an object")
        _check_schema_keywords(child, f"{path}/items", root)

    if "oneOf" in schema:
        branches = schema["oneOf"]
        if not isinstance(branches, list) or not branches:
            raise SchemaFailure(f"schema keyword oneOf at {path} must be a non-empty array")
        for index, child in enumerate(branches):
            _check_schema_keywords(child, f"{path}/oneOf/{index}", root)

    for key in ("minItems", "maxItems", "minLength", "maxLength"):
        if key in schema and (not isinstance(schema[key], int) or isinstance(schema[key], bool) or schema[key] < 0):
            raise SchemaFailure(f"schema keyword {key} at {path} must be a non-negative integer")
    for key in ("minimum", "maximum"):
        if key in schema and (not isinstance(schema[key], (int, float)) or isinstance(schema[key], bool)):
            raise SchemaFailure(f"schema keyword {key} at {path} must be a number")
    if "uniqueItems" in schema and not isinstance(schema["uniqueItems"], bool):
        raise SchemaFailure(f"schema keyword uniqueItems at {path} must be boolean")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise SchemaFailure(f"schema keyword enum at {path} must be a non-empty array")
    if "pattern" in schema:
        try:
            re.compile(schema["pattern"])
        except re.error as exc:
            raise SchemaFailure(f"invalid schema pattern at {path}: {exc}") from exc
    if "format" in schema and schema["format"] != "date-time":
        raise SchemaFailure(f"unsupported schema format at {path}: {schema['format']}")


def load_schema(source: Path | str | dict[str, Any] = SCHEMA_PATH) -> dict[str, Any]:
    if isinstance(source, dict):
        schema = source
    else:
        try:
            schema = parse_json_bytes(Path(source).read_bytes())
        except (OSError, ParseFailure) as exc:
            raise SchemaFailure(f"cannot load normative schema: {exc}") from exc
    if not isinstance(schema, dict):
        raise SchemaFailure("normative schema root must be an object")
    _check_schema_keywords(schema)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise SchemaFailure("unsupported JSON Schema dialect")
    return schema


def _json_type_matches(value: Any, expected: str) -> bool:
    mapping = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "boolean": lambda x: isinstance(x, bool),
        "integer": lambda x: (
            isinstance(x, int) and not isinstance(x, bool)
        ) or (
            isinstance(x, float) and x.is_integer()
        ),
        "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "null": lambda x: x is None,
    }
    if expected not in mapping:
        raise SchemaFailure(f"unsupported schema type: {expected}")
    return mapping[expected](value)


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise SchemaFailure(f"external or malformed schema reference is unsupported: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise SchemaFailure(f"unresolvable schema reference: {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise SchemaFailure(f"schema reference does not target an object: {ref}")
    return node


def _schema_error(errors: list[ValidationError], code: str, path: str, message: str) -> None:
    errors.append(ValidationError(code, path or "/", message))


def _json_equal(left: Any, right: Any) -> bool:
    """Compare values using JSON Schema's JSON-value equality model."""
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_json_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    return left == right


def _validate_schema(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str, errors: list[ValidationError]) -> None:
    if "$ref" in schema:
        _validate_schema(value, _resolve_ref(root, schema["$ref"]), root, path, errors)
        return
    if "oneOf" in schema:
        branch_results: list[list[ValidationError]] = []
        for branch in schema["oneOf"]:
            branch_errors: list[ValidationError] = []
            _validate_schema(value, branch, root, path, branch_errors)
            branch_results.append(branch_errors)
        matches = sum(not branch_errors for branch_errors in branch_results)
        if matches != 1:
            # recordSlot has stable discriminators. Preserve the selected branch's
            # precise diagnostic without making branch selection permissive.
            if isinstance(value, dict) and "record_id" in value:
                errors.extend(branch_results[0])
            elif isinstance(value, dict) and "state" in value:
                errors.extend(branch_results[-1])
            elif not isinstance(value, dict) and branch_results:
                errors.extend(branch_results[0])
            else:
                _schema_error(errors, "SCHEMA_ONE_OF", path, f"value must match exactly one alternative; matched {matches}")
        return
    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if not any(_json_type_matches(value, item) for item in types):
            _schema_error(errors, "SCHEMA_TYPE", path, f"expected type {expected}")
            return
    if "const" in schema and not _json_equal(value, schema["const"]):
        _schema_error(errors, "SCHEMA_CONST", path, f"expected constant {schema['const']!r}")
    if "enum" in schema and not any(_json_equal(value, item) for item in schema["enum"]):
        _schema_error(errors, "SCHEMA_ENUM", path, f"unknown token {value!r}")
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                _schema_error(errors, "SCHEMA_REQUIRED", f"{path}/{key}", "required property is missing")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if key in properties:
                _validate_schema(child, properties[key], root, child_path, errors)
            elif additional is False:
                _schema_error(errors, "SCHEMA_ADDITIONAL_PROPERTY", child_path, "unknown property is forbidden")
            elif isinstance(additional, dict):
                _validate_schema(child, additional, root, child_path, errors)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            _schema_error(errors, "SCHEMA_MIN_ITEMS", path, "array is shorter than minItems")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            _schema_error(errors, "SCHEMA_MAX_ITEMS", path, "array is longer than maxItems")
        if schema.get("uniqueItems"):
            if any(_json_equal(value[left], value[right]) for left in range(len(value)) for right in range(left + 1, len(value))):
                _schema_error(errors, "SCHEMA_UNIQUE_ITEMS", path, "array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, root, f"{path}/{index}", errors)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            _schema_error(errors, "SCHEMA_MIN_LENGTH", path, "string is shorter than minLength")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            _schema_error(errors, "SCHEMA_MAX_LENGTH", path, "string is longer than maxLength")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            _schema_error(errors, "SCHEMA_PATTERN", path, "string does not match required pattern")
        if schema.get("format") == "date-time":
            try:
                _timestamp(value)
            except ValueError:
                _schema_error(errors, "SCHEMA_FORMAT", path, "timestamp must be RFC 3339 UTC with Z suffix")
        elif "format" in schema:
            raise SchemaFailure(f"unsupported schema format: {schema['format']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            _schema_error(errors, "SCHEMA_MINIMUM", path, "number is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            _schema_error(errors, "SCHEMA_MAXIMUM", path, "number is above maximum")


def _timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("UTC Z timestamp required")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed


def _add(errors: list[ValidationError], code: str, path: str, message: str) -> None:
    errors.append(ValidationError(code, path, message))


def _semantic_validation(trace: dict[str, Any], errors: list[ValidationError]) -> str:
    """Validate only CDTS-owned structure, pins, and boundary assertions."""
    ids: dict[str, str] = {}

    def register(value: str, path: str) -> None:
        if value in ids:
            _add(errors, "DUPLICATE_ID", path, f"ID duplicates {ids[value]}")
        else:
            ids[value] = path

    register(trace["trace_id"], "/trace_id")
    register(trace["trace_scope"]["scope_id"], "/trace_scope/scope_id")
    refs: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(trace["record_refs"]):
        path = f"/record_refs/{index}"
        register(record["ref_id"], path + "/ref_id")
        refs[record["ref_id"]] = record
        owner = record["owner"]
        if record["specification_revision"] != PINNED_SOURCES[owner][1]:
            _add(errors, "REFERENCE_PIN_MISMATCH", path + "/specification_revision", "reference revision does not match its fixed owner source")
        if owner == "PCA" and record["record_type"] == "linkage_record":
            _add(errors, "PCA_LINKAGE_SUPERSEDED", path + "/record_type", "the pinned PCA Core does not define a current Linkage Record; use a CDTS linkage assertion")
    for index, absence in enumerate(trace["absences"]):
        register(absence["absence_id"], f"/absences/{index}/absence_id")
    links: dict[str, dict[str, Any]] = {}
    for index, link in enumerate(trace["linkage_assertions"]):
        path = f"/linkage_assertions/{index}"
        register(link["linkage_id"], path + "/linkage_id")
        links[link["linkage_id"]] = link
        for field in ("from_ref", "to_ref"):
            if link[field] not in refs:
                _add(errors, "DANGLING_REFERENCE", path + "/" + field, "link endpoint does not resolve to a local ref_id")
        if link["from_ref"] == link["to_ref"]:
            _add(errors, "SELF_LINK", path, "self-links are not admissible")
        for evidence_ref in link["evidence_refs"]:
            if evidence_ref not in refs:
                _add(errors, "DANGLING_REFERENCE", path + "/evidence_refs", f"unknown evidence ref_id: {evidence_ref}")
        if link["relationship"] in {"cdts.precedes", "cdts.follows"} and link["from_ref"] in refs and link["to_ref"] in refs:
            left = _timestamp(refs[link["from_ref"]]["recorded_at"])
            right = _timestamp(refs[link["to_ref"]]["recorded_at"])
            ordered = left < right if link["relationship"] == "cdts.precedes" else left > right
            if not ordered:
                _add(errors, "TEMPORAL_ORDER", path, "temporal assertion contradicts referenced record timestamps")
    for index, conflict in enumerate(trace["conflicts"]):
        path = f"/conflicts/{index}"
        register(conflict["conflict_id"], path + "/conflict_id")
        for ref_id in conflict["record_refs"]:
            if ref_id not in refs:
                _add(errors, "DANGLING_REFERENCE", path + "/record_refs", f"unknown ref_id: {ref_id}")
        positioned_refs = [position["record_ref"] for position in conflict["positions"]]
        for position in conflict["positions"]:
            if position["record_ref"] not in refs:
                _add(errors, "DANGLING_REFERENCE", path + "/positions", f"unknown position ref_id: {position['record_ref']}")
        if len(positioned_refs) != len(conflict["record_refs"]) or set(positioned_refs) != set(conflict["record_refs"]):
            _add(errors, "CONFLICT_POSITION_MISMATCH", path + "/positions", "positions must cover each declared conflict record exactly once")
        if conflict["resolution"] == "selected_for_local_decision" and not conflict["precedence_policy_ref"]:
            _add(errors, "CONFLICT_POLICY_REQUIRED", path + "/precedence_policy_ref", "a local selection requires an external policy reference")
    for index, item in enumerate(trace["unresolved"]):
        register(item["unresolved_id"], f"/unresolved/{index}/unresolved_id")
        for link_ref in item["linkage_refs"]:
            if link_ref not in links:
                _add(errors, "DANGLING_REFERENCE", f"/unresolved/{index}/linkage_refs", f"unknown linkage_id: {link_ref}")

    source_by_owner: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(trace["source_revisions"]):
        path = f"/source_revisions/{index}"
        owner = source["owner"]
        if owner in source_by_owner:
            _add(errors, "DUPLICATE_SOURCE", path, f"duplicate source pin for {owner}")
            continue
        source_by_owner[owner] = source
        repository, revision, role = PINNED_SOURCES[owner]
        if source["repository"] != repository:
            _add(errors, "SOURCE_OWNER_MISMATCH", path + "/repository", "repository does not match source owner")
        if source["revision"] != revision:
            _add(errors, "SOURCE_PIN_MISMATCH", path + "/revision", "revision does not match fixed source")
        if source["role"] != role:
            _add(errors, "SOURCE_ROLE_MISMATCH", path + "/role", f"{owner} must have role {role}")
    required_owners = {record["owner"] for record in trace["record_refs"]} | {"REVIEW_PROTOCOL"}
    for owner in required_owners:
        if owner not in source_by_owner:
            _add(errors, "SOURCE_PIN_REQUIRED", "/source_revisions", f"a fixed source pin is required for {owner}")

    observed_from = _timestamp(trace["trace_scope"]["observed_from"])
    observed_to = _timestamp(trace["trace_scope"]["observed_to"])
    if observed_from > observed_to:
        _add(errors, "SCOPE_INTERVAL", "/trace_scope", "observed_from must not be later than observed_to")
    if _timestamp(trace["provenance"]["produced_at"]) < observed_from:
        _add(errors, "PROVENANCE_TIME", "/provenance/produced_at", "trace production cannot predate the observed scope")

    revision = trace["trace_revision"]
    amendments = trace["amendments"]
    if revision == 1 and amendments:
        _add(errors, "AMENDMENT_UNEXPECTED", "/amendments", "revision 1 cannot have amendment history")
    if revision > 1 and not amendments:
        _add(errors, "AMENDMENT_REQUIRED", "/amendments", "later revisions must preserve prior revision digests")
    if amendments:
        expected = 1
        for index, amendment in enumerate(amendments):
            if amendment["from_revision"] != expected or amendment["to_revision"] != expected + 1:
                _add(errors, "AMENDMENT_CHAIN", f"/amendments/{index}", "amendments must form a contiguous chain from revision 1")
            expected = amendment["to_revision"]
        if expected != revision:
            _add(errors, "AMENDMENT_CHAIN", "/amendments", "amendment chain must end at trace_revision")

    if trace["conflicts"] and trace["unresolved"]:
        return "ADMISSIBLE_WITH_CONFLICTS_AND_UNRESOLVED"
    if trace["conflicts"]:
        return "ADMISSIBLE_WITH_CONFLICTS"
    if trace["unresolved"]:
        return "ADMISSIBLE_WITH_UNRESOLVED"
    return "ADMISSIBLE"


def validate_data(data: Any, schema: dict[str, Any] | None = None) -> ValidationResult:
    schema = schema or load_schema()
    errors: list[ValidationError] = []
    _validate_schema(data, schema, schema, "", errors)
    if errors or not isinstance(data, dict):
        return ValidationResult("INVALID", tuple(errors))
    derived = _semantic_validation(data, errors)
    return ValidationResult("INVALID" if errors else derived, tuple(errors))


def validate_file(path: Path | str) -> ValidationResult:
    try:
        data = parse_json_bytes(Path(path).read_bytes())
    except OSError as exc:
        raise ParseFailure(f"cannot read input: {exc}") from exc
    return validate_data(data)


def _exit_code(status: str) -> int:
    return {"ADMISSIBLE": 0, "INVALID": 1, "ADMISSIBLE_WITH_CONFLICTS": 3, "ADMISSIBLE_WITH_UNRESOLVED": 4, "ADMISSIBLE_WITH_CONFLICTS_AND_UNRESOLVED": 5}.get(status, 2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate one CDTS v0.1-draft JSON record.")
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result")
    args = parser.parse_args(argv)
    try:
        result = validate_file(args.record)
        payload = result.as_dict()
        code = _exit_code(result.status)
    except ParseFailure as exc:
        payload = {"status": "INVALID", "valid": False, "world_truth": "NOT_EVALUATED", "errors": [{"code": "PARSE_FAILURE", "path": "/", "message": str(exc)}]}
        code = 2
    except SchemaFailure as exc:
        payload = {"status": "TOOL_FAILURE", "valid": False, "world_truth": "NOT_EVALUATED", "errors": [{"code": "SCHEMA_FAILURE", "path": "/", "message": str(exc)}]}
        code = 2
    if args.json:
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    else:
        print(payload["status"])
        for error in payload["errors"]:
            print(f"{error['code']} {error['path']}: {error['message']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
