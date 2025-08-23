# tests/test_agents.py (NEW)
import pytest
from backend.agent_registry import AgentRegistry

@pytest.fixture
def registry():
    return AgentRegistry()

def test_lead_generation(registry):
    result = registry.execute_action(
        "lead_generation",
        "process_web_lead",
        {"form_data": {"name": "John", "email": "john@test.com"}}
    )
    assert "name" in result["result"]
    assert "email" in result["result"]
    assert result["review"]["score"] > 90