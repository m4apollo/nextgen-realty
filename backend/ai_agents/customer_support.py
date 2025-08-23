from .base_agent import AIAgent
from utils.logging import logger

class CustomerSupportAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Customer Support Agent",
            role="Handle real-time customer inquiries and support",
            model="llama3"
        )
        self.knowledge_base = {
            "pricing": "We offer Free, Pro ($29/mo), and Team ($99/mo) plans",
            "features": "AI follow-ups, appointment scheduling, lead management",
            "onboarding": "Check our tutorial videos at help.nextgenrealty.com"
        }
    
    def handle_inquiry(self, question: str, context: dict = None) -> str:
        """Respond to customer support questions"""
        # Check knowledge base first
        question_lower = question.lower()
        for keyword, response in self.knowledge_base.items():
            if keyword in question_lower:
                return response
        
        # Generate custom response
        prompt = (
            f"Respond to this customer support inquiry as {settings.COMPANY_NAME}:\n"
            f"Question: {question}\n\n"
            "Requirements:\n"
            "- 2-3 sentences maximum\n"
            "- Helpful and professional tone\n"
            "- Offer further assistance if needed"
        )
        
        return self.query(prompt)
    
    def escalate_issue(self, issue: dict) -> dict:
        """Escalate complex issues to human support"""
        prompt = (
            "Create a summary of this customer issue for human support:\n"
            f"Issue: {issue}\n\n"
            "Requirements:\n"
            "- Identify key problem\n"
            "- Note customer sentiment\n"
            "- Suggest resolution approach"
        )
        
        return {"summary": self.query(prompt), "status": "escalated"}