from .base_agent import AIAgent

class ComplianceAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Compliance Agent",
            role="Ensure adherence to real estate regulations",
            model="llama3"
        )
        self.compliance_rules = {
            "advertising": [
                "Clear disclosure of brokerage relationship",
                "No false or misleading statements",
                "Fair Housing Act compliance"
            ],
            "transactions": [
                "Proper disclosure of material facts",
                "Accurate representation of property",
                "CAN-SPAM compliance for email"
            ]
        }
    
    def review_content(self, content: str, content_type: str) -> dict:
        """Review marketing/content for compliance"""
        rules = "\n".join(self.compliance_rules.get(content_type, []))
        
        prompt = (
            f"Review this {content_type} content for compliance:\n"
            f"Content: {content}\n\n"
            f"Compliance Rules:\n{rules}\n\n"
            "Provide:\n"
            "- Compliance status (pass/fail)\n"
            "- Specific issues found\n"
            "- Recommended fixes\n"
            "- Risk assessment"
        )
        
        return {"review": self.query(prompt)}
    
    def generate_disclosure(self, transaction_type: str, jurisdiction: str) -> str:
        """Generate required legal disclosures"""
        prompt = (
            f"Create {jurisdiction} real estate disclosure for {transaction_type}:\n\n"
            "Requirements:\n"
            "- Include all legally required elements\n"
            "- Clear, plain language\n"
            "- Proper formatting\n"
            "- Brokerage information footer"
        )
        
        return self.query(prompt)