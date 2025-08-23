from .base_agent import AIAgent
from utils.email import send_email
from utils.logging import logger
import datetime

class OnboardingAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Onboarding Agent",
            role="Guide new users through product adoption",
            model="mistral"
        )
        self.sequence = [
            {"delay": 0, "template": "welcome"},
            {"delay": 1, "template": "feature_tour"},
            {"delay": 3, "template": "tips"},
            {"delay": 7, "template": "advanced_features"}
        ]
    
    def send_welcome_email(self, user: dict) -> dict:
        """Send initial welcome email"""
        prompt = (
            f"Create welcome email for new {settings.COMPANY_NAME} user:\n"
            f"Name: {user['full_name']}\n"
            f"Plan: {user.get('plan', 'free')}\n\n"
            "Requirements:\n"
            "- Warm welcome\n"
            "- Key next steps\n"
            "- Getting started tips\n"
            "- Support resources\n"
            "- Professional but friendly tone"
        )
        
        email_content = self.query(prompt)
        subject = f"Welcome to {settings.COMPANY_NAME}!"
        
        # Send email
        if settings.SENDGRID_API_KEY:
            send_email(user['email'], subject, email_content)
            return {"status": "sent"}
        else:
            logger.warning("Email sending disabled - simulation mode")
            return {"status": "simulated", "content": email_content}
    
    def generate_tutorial(self, user_type: str = "realtor") -> dict:
        """Create customized onboarding tutorial"""
        prompt = (
            f"Create step-by-step onboarding tutorial for {user_type}:\n\n"
            "Structure:\n"
            "1. Account setup\n"
            "2. Lead import\n"
            "3. AI follow-up configuration\n"
            "4. Reporting features\n"
            "5. Tips for success\n\n"
            "Use clear headings and bullet points"
        )
        
        return {"tutorial": self.query(prompt)}