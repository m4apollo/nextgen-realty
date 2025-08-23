from .base_agent import AIAgent
import requests
from utils.logging import logger
import subprocess

class CybersecurityAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Cybersecurity Agent",
            role="Monitor and protect system security",
            model="mistral"
        )
    
    def check_vulnerabilities(self) -> dict:
        """Perform basic security scan"""
        results = {}
        
        # Check for common vulnerabilities
        try:
            # Dependency scan (simplified)
            vuln_scan = subprocess.run(
                ['npm', 'audit', '--json'], 
                capture_output=True, 
                text=True
            )
            results['dependency_scan'] = json.loads(vuln_scan.stdout)
        except Exception as e:
            logger.error(f"Vulnerability scan failed: {str(e)}")
            results['dependency_scan'] = {"error": str(e)}
        
        # Generate security report
        prompt = (
            "Analyze these security scan results and provide recommendations:\n"
            f"Results: {results}\n\n"
            "Focus on:\n"
            "- Critical vulnerabilities\n"
            "- Data protection issues\n"
            "- Compliance gaps (GDPR, CCPA)\n"
            "- Actionable fixes"
        )
        
        results['recommendations'] = self.query(prompt)
        return results
    
    def detect_anomalies(self, log_data: str) -> dict:
        """Analyze system logs for security threats"""
        prompt = (
            "Analyze these system logs for security anomalies:\n"
            f"Logs: {log_data[:2000]}\n\n"
            "Identify:\n"
            "- Unauthorized access attempts\n"
            "- Suspicious patterns\n"
            "- Potential breaches\n"
            "- Recommended actions"
        )
        
        return {"analysis": self.query(prompt)}