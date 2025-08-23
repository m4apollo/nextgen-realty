from .base_agent import AIAgent
from utils.email import send_email
from utils.logging import logger
import datetime

class FollowUpAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Follow-Up Agent",
            role="Automate lead nurturing through timely follow-ups",
            model="llama3"
        )
        self.sequence = {
            1: {"days_after": 1, "template": "initial_followup"},
            2: {"days_after": 3, "template": "value_proposition"},
            3: {"days_after": 7, "template": "final_offer"}
        }
    
    def send_followup(self, lead: dict, sequence_step: int) -> dict:
        """Send follow-up email based on sequence position"""
        step_config = self.sequence.get(sequence_step)
        if not step_config:
            return {"error": "Invalid sequence step"}
        
        prompt = (
            f"Create follow-up email for real estate lead (step {sequence_step}):\n"
            f"Lead: {lead}\n\n"
            "Requirements:\n"
            f"- Reference previous communication\n"
            f"- Provide new value (market insights, tips)\n"
            f"- Gentle call-to-action\n"
            f"- Signature: {settings.COMPANY_NAME} Team"
        )
        
        email_content = self.query(prompt)
        subject = f"Following up on your real estate interests"
        
        # Send email
        if settings.SENDGRID_API_KEY:
            send_email(lead['email'], subject, email_content)
            return {"status": "sent", "step": sequence_step, "to": lead['email']}
        else:
            logger.warning("Email sending disabled - simulation mode")
            return {"status": "simulated", "content": email_content}