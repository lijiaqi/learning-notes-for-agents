import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class HelloLLMAgent:
    def __init__(self, model:str=None, api_key:str=None):
        self.model = model or os.getenv("LLM_MODEL_NAME")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL")
        self.timeout = os.getenv("LLM_TIMEOUT")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

    def think(self, messages:list[dict], temperature:float=0.7):
        print(f"Thinking about: {messages}")
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = temperature,
                stream=True
            )
            