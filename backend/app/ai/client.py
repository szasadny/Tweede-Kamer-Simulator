import httpx
import os
from typing import Dict, List, Any, Optional
from app.config import settings

class MistralClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.MISTRAL_API_KEY
        self.api_url = settings.MISTRAL_API_URL
        self.model = "mistral-small-latest"  # Default model
    
    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generate a response from the Mistral AI API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
            
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
