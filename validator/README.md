# Reference Validator

Requires Python 3.11+ and only the standard library.

```bash
python validator/cdts_validate.py path/to/trace.json
python validator/cdts_validate.py --json path/to/trace.json
python -m unittest discover -v
```

The validator loads the canonical schema, supports a deliberately small audited JSON Schema keyword subset, and treats any unsupported normative assertion as `TOOL_FAILURE`. Its result is derived; a trace cannot include a self-awarded validation field. External authenticity, native-spec validity, and world truth are outside scope.
