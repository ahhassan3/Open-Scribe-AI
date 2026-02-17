import json
from urllib.parse import urlparse

import httpx

from apps.api.core.config import get_settings


class LLMOrchestrator:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _validate_local_only(self) -> None:
        if self.settings.allow_cloud_llm:
            return

        parsed = urlparse(self.settings.ollama_base_url)
        hostname = (parsed.hostname or "").lower()
        if not hostname or hostname not in self.settings.local_llm_host_allowlist:
            raise ValueError("Local-only inference enforced: non-local Ollama host is not allowed")

    def generate_json(self, prompt: str) -> dict:
        self._validate_local_only()
        payload = {
            "model": self.settings.llm_model,
            "format": "json",
            "stream": False,
            "prompt": prompt,
            "options": {"temperature": 0.2},
        }
        endpoint = f"{self.settings.ollama_base_url}/api/generate"
        for _ in range(2):
            response = httpx.post(endpoint, json=payload, timeout=self.settings.llm_timeout_seconds)
            response.raise_for_status()
            data = response.json()
            text = data.get("response", "{}")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue
        raise ValueError("LLM did not return valid JSON")
