from .base_agent import AIAgent
from datetime import datetime

class AnalyticsAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Analytics Agent",
            role="Track performance metrics and conduct quality reviews",
            model="llama3"
        )
    
    def generate_dashboard_report(self, period: str = "daily") -> dict:
        prompt = (
            f"Create a comprehensive {period} performance report for NextGen Realty. "
            "Include key metrics, insights, and recommendations."
        )
        return {
            "period": period,
            "report": self.query(prompt),
            "generated_at": datetime.utcnow()
        }
    
    def quality_review(self, agent_output: dict, context: dict) -> dict:
        prompt = (
            "Conduct professional quality review for this agent output: "
            f"{agent_output}. Context: {context}. "
            "Evaluate for accuracy, compliance, and effectiveness. "
            "Provide score (0-100) and specific recommendations."
        )
        return self.query(prompt)