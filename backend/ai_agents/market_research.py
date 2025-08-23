from .base_agent import BaseAgent
from schemas import MarketReport, CompetitiveAnalysis

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            model="mistral",
            system_prompt=(
                "Specialize in real estate market analysis. Provide competitive intelligence, "
                "pricing trends, neighborhood analytics, and investment opportunity reports. "
                "Use data from MLS, Zillow, and public records."
            )
        )
    
    def execute(self, task: dict) -> MarketReport:
        analysis_type = task.get("analysis_type")
        location = task["location"]
        
        if analysis_type == "competition":
            return self._analyze_competition(location)
        elif analysis_type == "pricing_trends":
            return self._generate_pricing_report(location)
        
    def _analyze_competition(self, location: str) -> CompetitiveAnalysis:
        prompt = f"""Provide competitive analysis for {location} including:
        1. Top 5 competing agents
        2. Average days on market
        3. Pricing strategies
        4. Marketing tactics
        5. Service differentiators"""
        
        response = self.llm.generate(prompt)
        return CompetitiveAnalysis(
            location=location,
            content=response,
            data_sources=["MLS", "ZillowAPI", "PublicRecords"]
        )