from abc import ABC, abstractmethod
from app.app import OPENAI_API_KEY
from app.constants import GPT_MODEL, GPT_MODEL_MINI_TTS, GPT_MODEL_MINI_TTS_REALTIME
from openai import OpenAI


class LLMClient(ABC):
    """Generic LLM client interface for provider-agnostic usage"""

    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def create_client(self):
        pass


class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = None
        self.openai_key = OPENAI_API_KEY
        self.gpt_model: str = GPT_MODEL
        self.tts_model: str = GPT_MODEL_MINI_TTS
        self.tts_realtime_model: str = GPT_MODEL_MINI_TTS_REALTIME

        self.temperature: float = 0.8
        self.speed: float = 1

        self.create_client()  # runs immediately

    def create_client(self):
        try:
            self.client = OpenAI(api_key=self.openai_key)
            print("openai client initialized")
            return self.client
        except Exception as e:
            raise Exception("unable to initialize openai client: ", e)
