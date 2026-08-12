import json
from typing import Any
from urllib.parse import parse_qsl, urlencode

SENSITIVE_KEYS = frozenset({"password", "birthdate", "access_token"})


def _redact_value(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            key: ("***" if key.lower() in SENSITIVE_KEYS else _redact_value(value))
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_redact_value(item) for item in data]
    return data


def redact_body(body: str, content_type: str | None = None) -> str:
    if not body:
        return "-"

    content_type = (content_type or "").lower()

    if "application/json" in content_type or body.lstrip().startswith(("{", "[")):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            return body
        return json.dumps(_redact_value(parsed), ensure_ascii=False)

    if "application/x-www-form-urlencoded" in content_type or "=" in body:
        pairs = parse_qsl(body, keep_blank_values=True)
        redacted = [
            (key, "***" if key.lower() in SENSITIVE_KEYS else value)
            for key, value in pairs
        ]
        return urlencode(redacted)

    return body
