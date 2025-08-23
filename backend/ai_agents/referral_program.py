from .base_agent import BaseAgent
from schemas import ReferralProgram, IncentiveStructure

class ReferralManager(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ReferralManager",
            model="mistral",
            system_prompt=(
                "Design and manage referral programs to drive viral growth. "
                "Create incentive structures, tracking mechanisms, and "
                "automated reward systems."
            )
        )
    
    def execute(self, params: dict) -> ReferralProgram:
        prompt = f"""Create referral program with:
        - Target audience: {params.get('audience', 'existing_clients')}
        - Primary incentive: {params.get('incentive_type', 'cash_reward')}
        - Budget: ${params.get('budget', 5000)}
        - Duration: {params.get('duration', '30 days')}
        
        Include:
        - Tracking codes
        - Reward tiers
        - Automated payout triggers
        - Compliance safeguards"""
        
        response = self.llm.generate(prompt)
        return ReferralProgram(
            program_details=response,
            incentive_structure=IncentiveStructure(
                base_reward=100,
                bonus_threshold=3,
                max_reward=500
            )
        )