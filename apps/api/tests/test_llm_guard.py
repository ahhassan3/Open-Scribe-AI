import pytest

from apps.api.services.llm_orchestrator import LLMOrchestrator


def test_llm_guard_rejects_non_local_hostname():
    orch = LLMOrchestrator()
    orch.settings.allow_cloud_llm = False
    orch.settings.ollama_base_url = "https://localhost.attacker.com"
    orch.settings.local_llm_host_allowlist_raw = "localhost,127.0.0.1,::1,ollama"

    with pytest.raises(ValueError):
        orch._validate_local_only()


def test_llm_guard_allows_local_hostname():
    orch = LLMOrchestrator()
    orch.settings.allow_cloud_llm = False
    orch.settings.ollama_base_url = "http://ollama:11434"
    orch.settings.local_llm_host_allowlist_raw = "localhost,127.0.0.1,::1,ollama"

    orch._validate_local_only()
