from __future__ import annotations

import csv
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark"
EXPERIMENTS_DIR = REPO_ROOT / "experiments"
PROMPTS_DIR = EXPERIMENTS_DIR / "prompts"
SCHEMAS_DIR = EXPERIMENTS_DIR / "schemas"
RESULTS_DIR = REPO_ROOT / "results" / "experiments"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"

TRIGGER_CASE_COLUMNS = [
    "case_id",
    "user_request",
    "expected_label",
    "relevant_skill",
    "reason",
]

RISK_CASE_COLUMNS = [
    "case_id",
    "risk_type",
    "example",
    "expected_detection",
    "relevant_artifact",
    "reason",
]

SKILL_SAMPLE_COLUMNS = [
    "artifact_name",
    "repository_url",
    "purpose",
    "metadata",
    "trigger_contract",
    "instructions",
    "context_boundary",
    "execution_constraints",
    "memory_interface",
    "tests",
    "security_checks",
    "failure_modes",
    "notes",
]

ALLOWED_TRIGGER_LABELS = {
    "should_trigger",
    "should_not_trigger",
    "ambiguous",
}

REQUIRED_PROVIDER_ENV_VARS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "LONGCAT_API_KEY",
)

KNOWN_PROVIDER_PREFIXES = (
    "OPENAI",
    "ANTHROPIC",
    "LONGCAT",
    "GOOGLE",
    "GEMINI",
    "MISTRAL",
    "COHERE",
    "GROQ",
    "TOGETHER",
    "FIREWORKS",
    "OPENROUTER",
    "DEEPSEEK",
    "XAI",
    "AZURE_OPENAI",
    "HUGGINGFACE",
    "HF",
)

CREDENTIAL_SUFFIXES = (
    "_API_KEY",
    "_ACCESS_TOKEN",
    "_AUTH_TOKEN",
    "_TOKEN",
)

PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    api_key: str
    model: str
    endpoint: str
    protocol: str


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def load_csv_rows(path: Path, required_columns: Sequence[str] | None = None) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if required_columns is not None and fieldnames != list(required_columns):
            raise ValueError(
                f"Unexpected columns for {path}: expected {list(required_columns)!r}, got {fieldnames!r}"
            )
        return list(reader)


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def render_prompt_template(template_text: str, replacements: Mapping[str, str]) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    unresolved = PLACEHOLDER_PATTERN.findall(rendered)
    if unresolved:
        raise ValueError(f"Unresolved placeholders remain: {sorted(set(unresolved))}")
    return rendered


def write_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    ensure_directories([path.parent])
    with path.open("w", encoding="utf-8", newline="") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True))
            handle.write("\n")


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    ensure_directories([path.parent])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))


def safe_divide(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def precision_recall_f1(true_positive: int, false_positive: int, false_negative: int) -> dict[str, float | None]:
    precision = safe_divide(true_positive, true_positive + false_positive)
    recall = safe_divide(true_positive, true_positive + false_negative)
    if precision is None or recall is None or precision + recall == 0:
        f1 = None if precision is None or recall is None else 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def format_metric(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *body_rows])


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def filename_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def relative_display(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _env_has_value(name: str) -> bool:
    value = os.getenv(name, "")
    return bool(value and value.strip())


def detect_provider_env_vars() -> dict[str, bool]:
    statuses: dict[str, bool] = {
        name: _env_has_value(name)
        for name in REQUIRED_PROVIDER_ENV_VARS
    }
    extra_present: set[str] = set()
    for name, value in os.environ.items():
        upper_name = name.upper()
        if upper_name in statuses:
            continue
        if not value.strip():
            continue
        if upper_name.startswith(KNOWN_PROVIDER_PREFIXES) and upper_name.endswith(CREDENTIAL_SUFFIXES):
            extra_present.add(upper_name)
    for name in sorted(extra_present):
        statuses[name] = True
    return statuses


def any_provider_credentials_present(statuses: Mapping[str, bool] | None = None) -> bool:
    current_statuses = statuses or detect_provider_env_vars()
    return any(current_statuses.values())


def _join_url(base_url: str, suffix: str) -> str:
    return base_url.rstrip("/") + "/" + suffix.lstrip("/")


def resolve_provider_config(provider: str | None = None, model: str | None = None) -> tuple[ProviderConfig | None, str | None]:
    provider_name = (provider or "").strip().lower()
    available_providers = [
        candidate
        for candidate in ("openai", "anthropic", "longcat")
        if _env_has_value(f"{candidate.upper()}_API_KEY")
    ]

    if provider_name and provider_name not in {"openai", "anthropic", "longcat"}:
        return None, f"not run: unsupported provider {provider_name}"
    if not provider_name:
        if not available_providers:
            return None, "not run: missing credentials"
        provider_name = available_providers[0]

    env_name = f"{provider_name.upper()}_API_KEY"
    api_key = os.getenv(env_name, "").strip()
    if not api_key:
        return None, "not run: missing credentials"

    if provider_name == "openai":
        model_name = (model or os.getenv("OPENAI_MODEL", "")).strip()
        if not model_name:
            return None, "not run: missing model selection"
        endpoint = os.getenv("OPENAI_API_URL", "").strip()
        if not endpoint:
            base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
            endpoint = _join_url(base_url, "responses")
        return ProviderConfig("openai", api_key, model_name, endpoint, "openai_responses"), None

    if provider_name == "anthropic":
        model_name = (model or os.getenv("ANTHROPIC_MODEL", "")).strip()
        if not model_name:
            return None, "not run: missing model selection"
        endpoint = os.getenv("ANTHROPIC_API_URL", "").strip()
        if not endpoint:
            base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1").strip()
            endpoint = _join_url(base_url, "messages")
        return ProviderConfig("anthropic", api_key, model_name, endpoint, "anthropic_messages"), None

    model_name = (model or os.getenv("LONGCAT_MODEL", "")).strip()
    if not model_name:
        return None, "not run: missing model selection"
    endpoint = os.getenv("LONGCAT_API_URL", "").strip()
    if not endpoint:
        base_url = os.getenv("LONGCAT_BASE_URL", "").strip()
        if base_url:
            endpoint = _join_url(base_url, "chat/completions")
    if not endpoint:
        return None, "not run: missing provider configuration"
    return ProviderConfig("longcat", api_key, model_name, endpoint, "openai_chat_compatible"), None


def _post_json(url: str, headers: Mapping[str, str], payload: Mapping[str, Any], *, max_retries: int = 5) -> Any:
    import time as _time

    request_data = json.dumps(payload).encode("utf-8")
    last_error: Exception | None = None

    for attempt in range(max_retries + 1):
        request = urllib.request.Request(
            url=url,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                **headers,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                body = response.read().decode("utf-8")
            return json.loads(body)
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < max_retries:
                retry_after = error.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else min(2 ** attempt * 5, 120)
                _time.sleep(wait)
                last_error = error
                continue
            if error.code >= 500 and attempt < max_retries:
                _time.sleep(min(2 ** attempt * 2, 60))
                last_error = error
                continue
            details = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {error.code} calling {url}: {details}") from error
        except urllib.error.URLError as error:
            if attempt < max_retries:
                _time.sleep(min(2 ** attempt * 2, 60))
                last_error = error
                continue
            raise RuntimeError(f"Network error calling {url}: {error}") from error

    raise RuntimeError(f"Max retries exceeded calling {url}: {last_error}")


def _extract_openai_responses_text(response_json: Any) -> str:
    if isinstance(response_json, dict):
        output_text = response_json.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text

        chunks: list[str] = []
        for item in response_json.get("output", []):
            if not isinstance(item, dict):
                continue
            for content in item.get("content", []):
                if not isinstance(content, dict):
                    continue
                if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                    chunks.append(content["text"])
        if chunks:
            return "\n".join(chunks)
    raise RuntimeError("OpenAI response did not contain extractable text output")


def _extract_anthropic_text(response_json: Any) -> str:
    if isinstance(response_json, dict):
        chunks: list[str] = []
        for content in response_json.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") == "text" and isinstance(content.get("text"), str):
                chunks.append(content["text"])
        if chunks:
            return "\n".join(chunks)
    raise RuntimeError("Anthropic response did not contain extractable text output")


def _extract_chat_completion_text(response_json: Any) -> str:
    if not isinstance(response_json, dict):
        raise RuntimeError("Chat completion response was not a JSON object")
    choices = response_json.get("choices", [])
    if not choices:
        raise RuntimeError("Chat completion response did not include choices")
    message = choices[0].get("message", {})
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: list[str] = []
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
        if chunks:
            return "\n".join(chunks)
    raise RuntimeError("Chat completion response did not contain extractable text output")


def call_model(prompt: str, config: ProviderConfig) -> tuple[str, Any]:
    import time as _time
    _time.sleep(0.5)  # rate-limit guard: 0.5s between calls

    if config.protocol == "openai_responses":
        payload = {
            "model": config.model,
            "input": prompt,
            "temperature": 0,
        }
        response_json = _post_json(
            config.endpoint,
            headers={"Authorization": f"Bearer {config.api_key}"},
            payload=payload,
        )
        return _extract_openai_responses_text(response_json), response_json

    if config.protocol == "anthropic_messages":
        payload = {
            "model": config.model,
            "max_tokens": 700,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }
        response_json = _post_json(
            config.endpoint,
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
            },
            payload=payload,
        )
        return _extract_anthropic_text(response_json), response_json

    if config.protocol == "openai_chat_compatible":
        payload = {
            "model": config.model,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
        response_json = _post_json(
            config.endpoint,
            headers={"Authorization": f"Bearer {config.api_key}"},
            payload=payload,
        )
        return _extract_chat_completion_text(response_json), response_json

    raise RuntimeError(f"Unsupported provider protocol: {config.protocol}")


def parse_json_object(text: str) -> Any:
    candidate = text.strip()
    if not candidate:
        return None
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    start_index = candidate.find("{")
    if start_index == -1:
        return None

    depth = 0
    in_string = False
    escaping = False
    for index in range(start_index, len(candidate)):
        char = candidate[index]
        if in_string:
            if escaping:
                escaping = False
            elif char == "\\":
                escaping = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                snippet = candidate[start_index:index + 1]
                try:
                    return json.loads(snippet)
                except json.JSONDecodeError:
                    return None
    return None


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return False


def normalize_tag_list(values: Any, allowed_tags: Sequence[str]) -> list[str]:
    allowed = set(allowed_tags)
    if not isinstance(values, list):
        return []
    normalized = []
    for value in values:
        if not isinstance(value, str):
            continue
        tag = value.strip()
        if tag in allowed and tag not in normalized:
            normalized.append(tag)
    return normalized

