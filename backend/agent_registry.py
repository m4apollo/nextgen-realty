from ai_agents import *
from master_reviewer import MasterReviewer
from config import settings
from utils.logging import logger
from typing import Dict, Any

class AgentRegistry:
    _agents = None
    
    @classmethod
    def initialize(cls):
        if cls._agents is None:
            cls._agents = {
                "lead_generation": LeadGenerationAgent(),
                "zillow_finder": ZillowFinderAgent(),
                "cold_email": ColdEmailAgent(),
                "follow_up": FollowUpAgent(),
                "subscription_mgmt": SubscriptionMgmtAgent(),
                "in_app_purchase": InAppPurchaseAgent(),
                "customer_support": CustomerSupportAgent(),
                "payment_help": PaymentHelpAgent(),
                "tax_compliance": TaxComplianceAgent(),
                "cybersecurity": CybersecurityAgent(),
                "compliance": ComplianceAgent(),
                "onboarding": OnboardingAgent(),
                "multi_tenancy": MultiTenancyAgent(),
                "content_creation": ContentCreationAgent(),
                "market_research": MarketResearchAgent(),
                "ad_campaign": AdCampaignAgent(),
                "analytics": AnalyticsAgent(),
                "service_chain": ServiceChainAgent(),
                "integration_support": IntegrationSupportAgent(),
                "feedback": FeedbackAgent(),
                "referral_program": ReferralProgramAgent(),
                "partnership_mgmt": PartnershipMgmtAgent()
            }
            cls.reviewer = MasterReviewer()
            logger.info("Agent registry initialized with 22 agents")
    
    @classmethod
    def get_agent(cls, agent_name: str):
        cls.initialize()
        return cls._agents.get(agent_name.lower())
    
    @classmethod
    def execute_action(
        cls, 
        agent_name: str, 
        action: str, 
        data: Dict[str, Any],
        review: bool = True
    ) -> Dict[str, Any]:
        agent = cls.get_agent(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}
        
        if not hasattr(agent, action):
            return {"error": f"Action {action} not available for {agent_name}"}
        
        try:
            result = getattr(agent, action)(**data)
            
            if review:
                review_result = cls.reviewer.review_output(
                    agent_name, 
                    result, 
                    {"action": action, "input": data}
                )
                if review_result["status"] == "rejected":
                    return {
                        "status": "revision_required",
                        "review": review_result,
                        "original_result": result
                    }
            
            return {"status": "success", "result": result}
        except Exception as e:
            return {"error": str(e)}