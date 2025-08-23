from .base_agent import AIAgent
from datetime import datetime, timedelta

class TaxComplianceAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Tax Compliance Agent",
            role="Ensure tax compliance across jurisdictions",
            model="llama3"
        )
        self.tax_rates = {
            "US": {"federal": 0.21, "state": 0.05},
            "EU": {"vat": 0.20},
            "CA": {"gst": 0.05, "pst": 0.07}
        }
    
    def calculate_tax(self, amount: float, region: str, tax_type: str = None) -> dict:
        """Calculate applicable taxes"""
        region_rates = self.tax_rates.get(region.upper(), {})
        
        if tax_type:
            rate = region_rates.get(tax_type, 0)
            return {"tax": amount * rate, "rate": rate, "type": tax_type}
        
        # Calculate all applicable taxes
        taxes = {t: amount * r for t, r in region_rates.items()}
        total_tax = sum(taxes.values())
        return {"total_tax": total_tax, "breakdown": taxes}
    
    def generate_tax_report(self, transactions: list, period: str) -> dict:
        """Generate quarterly tax report"""
        prompt = (
            f"Create professional tax report for {settings.COMPANY_NAME}:\n"
            f"Period: {period}\n"
            f"Transactions: {len(transactions)} transactions\n"
            f"Total Revenue: ${sum(t['amount'] for t in transactions)}\n\n"
            "Report Structure:\n"
            "1. Summary of tax liabilities\n"
            "2. Breakdown by jurisdiction\n"
            "3. Payment deadlines\n"
            "4. Compliance recommendations\n\n"
            "Use formal business language"
        )
        
        return {
            "report": self.query(prompt),
            "generated_at": datetime.utcnow()
        }