from .base_agent import AIAgent
import stripe
from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentHelpAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Payment Help Agent",
            role="Resolve payment issues and refund requests",
            model="mistral"
        )
    
    def resolve_failed_payment(self, payment_intent_id: str) -> dict:
        """Handle failed payment recovery"""
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            customer = stripe.Customer.retrieve(payment_intent.customer)
            
            prompt = (
                f"Create payment failure resolution email for {customer.email}:\n"
                f"Amount: ${payment_intent.amount/100}\n"
                f"Reason: {payment_intent.last_payment_error.get('message', 'Unknown')}\n\n"
                "Requirements:\n"
                "- Apologize for inconvenience\n"
                "- Explain reason clearly\n"
                "- Provide payment retry link\n"
                "- Offer support contact\n"
                "- Professional tone"
            )
            
            return {
                "status": "processed",
                "email_content": self.query(prompt),
                "customer": customer.email
            }
        except stripe.error.StripeError as e:
            return {"error": str(e)}
    
    def process_refund(self, charge_id: str, reason: str) -> dict:
        """Handle refund requests"""
        try:
            refund = stripe.Refund.create(charge=charge_id, reason=reason)
            
            prompt = (
                f"Create refund confirmation email:\n"
                f"Amount: ${refund.amount/100}\n"
                f"Reason: {reason}\n\n"
                "Requirements:\n"
                "- Apologize for inconvenience\n"
                "- Confirm refund details\n"
                "- Express hope to serve again\n"
                "- Professional tone"
            )
            
            return {
                "status": "refunded",
                "email_content": self.query(prompt),
                "amount": refund.amount
            }
        except stripe.error.StripeError as e:
            return {"error": str(e)}