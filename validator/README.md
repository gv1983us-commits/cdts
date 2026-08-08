# CDTS Reference Validator

The validator implements record profile `0.1` for artifact version `0.2`.

It uses only the Python standard library at runtime.

```bash
python validator/cdts_validate.py path/to/trace.json
python validator/cdts_validate.py --json path/to/trace.json
python -m unittest discover -v
```

The validator loads the normative schema, supports a deliberately bounded audited JSON Schema keyword subset, and treats unsupported normative assertions as tool failure.

Its result is derived; a trace cannot contain a producer-authored validation field.

The validator is a reference implementation, not a sixth normative surface. External authenticity, native-spec validity, expected-record completeness, producer identity, causality, identity, and world truth are outside its result.
