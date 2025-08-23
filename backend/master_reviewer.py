from ai_agents.analytics import AnalyticsAgent
from config import settings
from utils.logging import logger

class MasterReviewer:
    QUALITY_STANDARDS = {
        "accuracy": 0.95,
        "compliance": ["NAR", "GDPR", "CCPA", "CAN-SPAM"],
        "tone": "professional",
        "engagement": "high"
    }
    
    def __init__(self):
        self.analytics_agent = AnalyticsAgent()
        logger.info("Master Quality Reviewer initialized")
    
    def review_output(
        self, 
        agent_name: str, 
        output: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Review agent output against quality standards"""
        review_prompt = (
            f"As the Master Quality Reviewer for {settings.COMPANY_NAME}, evaluate this output:\n"
            f"Agent: {agent_name}\n"
            f"Action: {context.get('action', 'Unknown')}\n"
            f"Output: {output}\n"
            f"Context: {context}\n\n"
            "Evaluation Criteria:\n"
            "1. Accuracy: Is the information factually correct?\n"
            "2. Compliance: Does it comply with NAR, GDPR, CCPA, CAN-SPAM?\n"
            "3. Tone: Is it professional and appropriate for real estate?\n"
            "4. Engagement: Will it effectively engage the recipient?\n"
            "5. Business Value: Does it align with our business goals?\n\n"
            "Provide:\n"
            "- Quality score (0-100)\n"
            "- Specific recommendations if score < 95\n"
            "- Overall assessment"
        )
        
        evaluation = self.analytics_agent.query(review_prompt)
        quality_score = self._extract_score(evaluation)
        
        if quality_score < 95:
            return {
                "status": "rejected",
                "score": quality_score,
                "feedback": evaluation,
                "recommendations": self._extract_recommendations(evaluation)
            }
        return {
            "status": "approved",
            "score": quality_score,
            "feedback": evaluation
        }
    
    def _extract_score(self, evaluation: str) -> int:
        """Extract quality score from evaluation text"""
        try:
            if "score:" in evaluation.lower():
                score_str = evaluation.lower().split("score:")[1].strip().split()[0]
                return int(score_str)
            elif "score is" in evaluation.lower():
                score_str = evaluation.lower().split("score is")[1].strip().split()[0]
                return int(score_str)
        except:
            pass
        return 90  # Default if extraction fails
    
    def _extract_recommendations(self, evaluation: str) -> list:
        """Extract actionable recommendations"""
        try:
            if "recommendations:" in evaluation.lower():
                recs = evaluation.split("Recommendations:")[1].strip()
                return [r.strip() for r in recs.split("\n") if r.strip()]
        except:
            pass
        return ["Improve output quality based on review feedback"]