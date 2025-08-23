from .base_agent import BaseAgent
from schemas import AdCampaign, PlatformPerformance

class AdManager(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AdManager",
            model="llama3",
            system_prompt=(
                "Expert in digital advertising for real estate. Create and optimize "
                "paid campaigns across Google Ads, Facebook/Instagram, and Zillow. "
                "Maximize ROI through continuous A/B testing and budget allocation."
            )
        )
    
    def execute(self, task: dict) -> AdCampaign:
        budget = task["budget"]
        property_type = task["property_type"]
        
        prompt = f"""Design {property_type} ad campaign with ${budget} budget:
        - Platform allocation strategy
        - Target audience segments
        - A/B test variations
        - KPI tracking plan"""
        
        response = self.llm.generate(prompt)
        return AdCampaign(
            campaign_plan=response,
            platforms=["GoogleAds", "Facebook", "ZillowPremier"],
            budget_allocation={
                "Google": budget * 0.5,
                "Facebook": budget * 0.3,
                "Zillow": budget * 0.2
            }
        )