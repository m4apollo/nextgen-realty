from .base_agent import AIAgent
import requests
from config import settings
from utils.logging import logger

class ZillowFinderAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Zillow Finder Agent",
            role="Discover and process real estate leads from Zillow",
            model="llama3"
        )
    
    def find_fsbo_listings(self, location: str, max_results: int = 20) -> list:
        """Find For Sale By Owner listings in a specific location"""
        if not settings.ZILLOW_API_KEY:
            return {"error": "Zillow API key not configured"}
        
        try:
            url = f"https://api.zillow.com/fsbo?location={location}&apikey={settings.ZILLOW_API_KEY}&maxResults={max_results}"
            response = requests.get(url)
            listings = response.json().get("results", [])
            return [self.process_listing(listing) for listing in listings]
        except Exception as e:
            logger.error(f"Zillow API error: {str(e)}")
            return []
    
    def process_listing(self, listing: dict) -> dict:
        """Convert Zillow listing into lead format"""
        prompt = (
            f"Convert this Zillow listing into a lead for {settings.COMPANY_NAME}:\n"
            f"Listing: {listing}\n\n"
            "Extract: name (owner), phone, email (if available), source=Zillow FSBO, "
            "notes=Include property details. Return as JSON object."
        )
        result = self.query(prompt)
        try:
            return json.loads(result)
        except:
            logger.error(f"Failed to parse listing data: {result}")
            return {
                "name": listing.get("ownerName", ""),
                "phone": listing.get("contactPhone", ""),
                "email": listing.get("contactEmail", ""),
                "source": "Zillow FSBO",
                "notes": f"Property: {listing.get('address', '')} - {listing.get('price', '')}"
            }