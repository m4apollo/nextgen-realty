from .base_agent import BaseAgent
from schemas import IntegrationSchema, APIConnection

class IntegrationSupport(BaseAgent):
    def __init__(self):
        super().__init__(
            name="IntegrationSupport",
            model="mistral",
            system_prompt=(
                "Technical specialist for third-party integrations. Configure and "
                "troubleshoot connections with CRM tools, MLS services, payment "
                "gateways, and marketing platforms."
            )
        )
    
    def execute(self, task: dict) -> IntegrationSchema:
        platform = task["platform"]
        auth_type = task.get("auth_type", "OAuth2")
        
        prompt = f"""Generate integration specification for {platform}:
        - Authentication: {auth_type}
        - Required endpoints
        - Data mapping rules
        - Error handling procedures
        - Rate limiting strategy"""
        
        response = self.llm.generate(prompt)
        return IntegrationSchema(
            platform=platform,
            configuration=response,
            test_cases=[
                "Connection test",
                "Data sync validation",
                "Error simulation"
            ]
        )