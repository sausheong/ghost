
from typing import List, Optional
import requests
import json

from langchain.llms.base import LLM

class Llama2API(LLM):
    model_name: str = "Llama-2"
    temperature: float = 0.7
    max_output_tokens: int = 512
    base_url: str = ""
    api_key: str = ""

    def __init__(
            self,
            temperature: float,
            max_output_tokens: int,
            base_url: str,
            api_key: str,                 
    ) -> str:
        super().__init__()
        self.base_url = base_url
        self.api_key = api_key
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature    
        

    @property
    def _llm_type(self) -> str:
        return "Llama2API"

    def _call(
        self,
        prompt: str,   
        stop: Optional[List[str]] = None,
    ) -> str:       
        url = self.base_url
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "X-API-KEY": self.api_key,
        }  
        data = {
            "instruction": prompt,
            "temperature": self.temperature,
            "max_new_tokens": self.max_output_tokens,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()