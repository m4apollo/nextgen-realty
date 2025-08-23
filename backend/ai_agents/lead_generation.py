from .base_agent import AIAgent
import csv
from io import StringIO
from utils.logging import logger

class LeadGenerationAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Lead Generation Agent",
            role="Capture and process incoming leads from various sources",
            model="mistral"
        )
    
    def process_web_lead(self, form_data: dict) -> dict:
        """Process web form submissions into standardized lead format"""
        prompt = (
            f"Convert this web form submission into a standardized lead format for {settings.COMPANY_NAME}:\n"
            f"Form Data: {form_data}\n\n"
            "Extract: name, email, phone, source=Web, notes (if any). "
            "Return as JSON object."
        )
        result = self.query(prompt)
        try:
            return json.loads(result)
        except:
            logger.error(f"Failed to parse lead data: {result}")
            return {
                "name": form_data.get("name", ""),
                "email": form_data.get("email", ""),
                "phone": form_data.get("phone", ""),
                "source": "Web",
                "notes": form_data.get("message", "")
            }
    
    def import_csv_leads(self, csv_data: str) -> list:
        """Import leads from CSV file"""
        reader = csv.DictReader(StringIO(csv_data))
        return [self.process_web_lead(row) for row in reader]