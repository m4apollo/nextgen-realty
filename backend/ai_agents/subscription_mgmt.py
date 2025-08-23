from .base_agent import AIAgent
from utils.email import send_email
from utils.logging import logger
import stripe
from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionMgmtAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Subscription Management Agent",
            role="Handle subscription lifecycle events",
            model="mistral"
        )
    
    def handle_upgrade(self, user: dict, new_plan: str) -> dict:
        """Process subscription upgrade"""
        prompt = (
            f"Create upgrade confirmation email for {user['email']}:\n"
            f"Old Plan: {user.get('plan', 'free')}\n"
            f"New Plan: {new_plan}\n\n"
            "Requirements:\n"
            "- Thank customer\n"
            "- Highlight new features\n"
            "- Provide support contact\n"
            "- Professional tone"
        )
        
        email_content = self.query(prompt)
        subject = f"Your {settings.COMPANY_NAME} subscription upgrade"
        
        # Send email
        if settings.SENDGRID_API_KEY:
            send_email(user['email'], subject, email_content)
        
        return {"status": "processed", "email_sent": bool(settings.SENDGRID_API_KEY)}
    
    def handle_downgrade(self, user: dict, reason: str = "") -> dict:
        """Process subscription downgrade with retention offer"""
        prompt = (
            f"Create downgrade email with retention offer for {user['email']}:\n"
            f"Current Plan: {user.get('plan', 'free')}\n"
            f"Downgrade Reason: {reason or 'not specified'}\n\n"
            "Requirements:\n"
            "- Express regret\n"
            "- Offer limited-time discount\n"
            "- Highlight benefits of current plan\n"
            "- Professional but empathetic tone"
        )
        
        email_content = self.query(prompt)
        subject = f"We'd love to keep you at {settings.COMPANY_NAME}"
        
        # Send email
        if settings.SENDGRID_API_KEY:
            send_email(user['email'], subject, email_content)
        
        return {"status": "processed", "retention_offer_sent": True}