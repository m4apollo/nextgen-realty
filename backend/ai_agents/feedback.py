from .base_agent import BaseAgent
from schemas import FeedbackReport, SentimentAnalysis

class FeedbackAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FeedbackAgent",
            model="llama3",
            system_prompt=(
                "Analyze customer feedback across multiple channels. Identify "
                "sentiment patterns, feature requests, and churn risks. Generate "
                "actionable insights reports."
            )
        )
    
    def execute(self, feedback_data: list) -> FeedbackReport:
        prompt = f"""Analyze customer feedback:
        {feedback_data}
        
        Provide:
        1. Sentiment score (1-5)
        2. Top 3 positive aspects
        3. Top 3 improvement areas
        4. Churn risk assessment
        5. Feature request clustering"""
        
        response = self.llm.generate(prompt)
        return FeedbackReport(
            analysis=response,
            sentiment_score=self._calculate_sentiment(response),
            priority_issues=self._extract_issues(response)
        )