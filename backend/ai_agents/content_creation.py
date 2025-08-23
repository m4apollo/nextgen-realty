from .base_agent import BaseAgent
from schemas import MarketingMaterial, SocialMediaPost

class ContentCreator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ContentCreator",
            model="llama3",
            system_prompt=(
                "You are a real estate marketing expert. Generate high-conversion "
                "marketing materials including property descriptions, social media posts, "
                "email newsletters, and blog content. Maintain brand voice consistency."
            )
        )
    
    def execute(self, task: dict) -> dict:
        content_type = task.get("content_type")
        property_details = task.get("property_details", {})
        
        if content_type == "property_description":
            return self._generate_property_desc(property_details)
        elif content_type == "social_media":
            return self._generate_social_post(property_details)
        # Additional content types handled here
        
    def _generate_property_desc(self, details: dict) -> MarketingMaterial:
        prompt = f"""Generate compelling property description for {details['address']} with:
        - Bedrooms: {details['beds']}
        - Bathrooms: {details['baths']}
        - Unique features: {details['features']}
        - Target audience: {details.get('audience', 'first-time buyers')}"""
        
        response = self.llm.generate(prompt)
        return MarketingMaterial(
            content=response,
            seo_optimized=True,
            compliance_checked=False
        )
    
    # Additional content generation methods