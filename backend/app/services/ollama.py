import base64
import json
from typing import Any, List

import httpx

from app.core import config
from app.schemas.ai import AIGenerateResponse


class OllamaError(RuntimeError):
    pass


def _extract_json_payload(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise OllamaError("AI response did not contain JSON")
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise OllamaError("AI response JSON was invalid") from exc


def _normalize_tags(raw_tags: Any) -> List[str]:
    if isinstance(raw_tags, list):
        tags = [str(tag).strip() for tag in raw_tags]
    elif isinstance(raw_tags, str):
        tags = [tag.strip() for tag in raw_tags.split(",")]
    else:
        tags = []
    return [tag for tag in tags if tag]


def generate_product_content(image_bytes: bytes) -> AIGenerateResponse:
    prompt = (
        "You are generating ecommerce product content from an image. "
        "Return JSON only with keys: title, description, category, tags. "
        "tags must be a JSON array of short strings."
    )

    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "images": [base64.b64encode(image_bytes).decode("ascii")],
    }

    url = f"{config.OLLAMA_URL.rstrip('/')}/api/generate"
    try:
        with httpx.Client(timeout=60) as client:
            response = client.post(url, json=payload)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise OllamaError("AI service request failed") from exc

    data = response.json()
    raw_text = data.get("response", "").strip()
    if not raw_text:
        raise OllamaError("AI response was empty")

    result = _extract_json_payload(raw_text)
    normalized = {
        "ai_title": result.get("title", ""),
        "ai_description": result.get("description", ""),
        "ai_category": result.get("category", ""),
        "ai_tags": _normalize_tags(result.get("tags", [])),
    }
    try:
        return AIGenerateResponse(**normalized)
    except Exception as exc:
        raise OllamaError("AI response did not match expected schema") from exc
