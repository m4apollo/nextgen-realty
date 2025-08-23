# backend/ai_agents/base_agent.py (UPDATE)
import hashlib
from functools import lru_cache

class AIAgent:
    @lru_cache(maxsize=1000)
    def cached_query(self, prompt: str) -> str:
        """Cache frequent queries"""
        return self.query(prompt)
    
    def query(self, prompt: str, use_cache: bool = True) -> str:
        if use_cache:
            cache_key = hashlib.md5(prompt.encode()).hexdigest()
            return self.cached_query(cache_key)
        # ... existing code ...
import ollama
from langchain_core.prompts import ChatPromptTemplate
from config import settings
from utils.logging import logger
import requests
import json

class AIAgent:
    def __init__(self, name: str, role: str, model: str = "mistral"):
        self.name = name
        self.role = role
        self.model = model
        self.system_prompt = f"You are {name}, {role} for {settings.COMPANY_NAME}. Respond professionally and accurately."
    
    def query_local(self, prompt: str, context: dict = None) -> str:
        """Query local Ollama model"""
        full_prompt = f"{self.system_prompt}\n\n{prompt}"
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': full_prompt}],
                options={'temperature': 0.5}
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Local model query failed: {str(e)}")
            return f"Error: {str(e)}"
    
    def query_cloud(self, prompt: str) -> str:
        """Query cloud-based DeepSeek model"""
        if not settings.DEEPSEEK_API_KEY:
            return "DeepSeek API key not configured"
        
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-r1",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/completions",
                headers=headers,
                data=json.dumps(payload)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"DeepSeek query failed: {str(e)}")
            return f"Error: {str(e)}"
    
    def query(self, prompt: str, context: dict = None, use_cloud: bool = False) -> str:
        """Main query method with fallback"""
        if use_cloud:
            return self.query_cloud(prompt)
        return self.query_local(prompt, context)