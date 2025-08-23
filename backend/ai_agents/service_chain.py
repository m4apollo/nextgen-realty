from .base_agent import BaseAgent
from schemas import EscalationPath, ServiceTicket

class ServiceChain(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ServiceChain",
            model="llama3",
            system_prompt=(
                "Handle complex customer service escalations. Determine appropriate "
                "resolution paths, assign priority levels, and maintain communication "
                "logs across support tiers."
            )
        )
    
    def execute(self, ticket: ServiceTicket) -> EscalationPath:
        prompt = f"""Process support escalation:
        Issue: {ticket.issue_description}
        Customer: {ticket.customer_name}
        Current Attempts: {ticket.attempt_count}
        Urgency: {ticket.urgency_level}
        
        Determine escalation path with:
        - Next support tier
        - Required expertise
        - SLAs
        - Suggested resolution steps"""
        
        response = self.llm.generate(prompt)
        return EscalationPath(
            ticket_id=ticket.id,
            action_plan=response,
            escalation_level=ticket.urgency_level + 1
        )