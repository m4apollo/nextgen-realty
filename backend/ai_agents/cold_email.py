from .base_agent import AIAgent
from utils.email import send_email
from utils.logging import logger
from config import settings

class ColdEmailAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Cold Email Agent",
            role="Send personalized outreach emails to potential clients",
            model="mistral"
        )
    
    def send_outreach(self, lead: dict, template: str = "default") -> dict:
        """Generate and send personalized cold email"""
        prompt = (
            f"Create a personalized cold email for this real estate lead:\n"
            f"Lead: {lead}\n\n"
            "Requirements:\n"
            "- 3-4 sentences maximum\n"
            "- Include personalized reference to their property interest\n"
            "- Professional but friendly tone\n"
            "- Include call-to-action for consultation\n"
            "- Signature: {settings.COMPANY_NAME} Team"
        )
        
        email_content = self.query(prompt)
        subject = f"Professional real estate services for {lead.get('property_type', 'your property')}"
        
        # Send email
        if settings.SENDGRID_API_KEY:
            send_email(lead['email'], subject, email_content)
            return {"status": "sent", "to": lead['email'], "content": email_content}
        else:
            logger.warning("Email sending disabled - no SendGrid API key")
            return {"status": "simulated", "content": email_content}