import json
from constants import GPT_MODEL
from openai import OpenAI
import os
from abc import ABC, abstractmethod
from constants import GPT_MODEL, GPT_MODEL_MINI_TTS, GPT_MODEL_MINI_TTS_REALTIME
from openai import OpenAI


class Actor:
    def __init__(self, name):
        self.name = name
        self.last_line = None


class Play:
    def __init__(self, title):
        self.title = title


class LLMClient(ABC):
    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def create_client(self):
        pass


class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = None
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gpt_model: str = GPT_MODEL
        self.tts_model: str = GPT_MODEL_MINI_TTS
        self.tts_realtime_model: str = GPT_MODEL_MINI_TTS_REALTIME
        self.temperature: float = 0.8
        self.speed: float = 1

        self.create_client()  # run immediately

    def create_client(self):
        try:
            self.client = OpenAI(api_key=self.openai_key)
            print("openai client initialized")
            return self.client
        except Exception as e:
            raise Exception("unable to initialize openai client: ", e)

    def check_user_line_is_valid(self, prompt, play_title):
        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            functions=[
                {
                    "name": "check_line",
                    "description": f"Check if the user's line is from {play_title}",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "is_valid": {
                                "type": "boolean",
                                "description": f"True if the line is actually in {play_title}, otherwise False",
                            }
                        },
                        "required": ["is_valid"],
                    },
                }
            ],
            function_call={"name": "check_line"},
        )

        structured_args = response.choices[0].message.function_call.arguments
        print("response: ", response, structured_args)
        return json.loads(structured_args)["is_valid"]

    def get_next_line(self, prompt):
        try:
            print("next line prompt: ", prompt)
            response = self.client.chat.completions.create(
                model=GPT_MODEL, messages=[{"role": "user", "content": prompt}]
            )
            ai_line = response.choices[0].message.content.strip()
            return ai_line
        except Exception as e:
            print("error when getting next line: ", e)


class Orchestrator:
    def __init__(self, llm_client, actor, play):
        self.llm_client = llm_client
        self.actor: Actor = actor
        self.play: Play = play
        self.history = []
        pass

    def set_play_and_actor(self, play_title: str, user_actor: str):
        try:
            self.actor.name = user_actor
            self.play.title = play_title
        except Exception as e:
            print("error when setting play and user: ", e)

    def get_next_line_prompt(self, last_user_line):
        return f"""
        The user is {self.actor.name} in the play {self.play.title}.
        You play all other characters.
        The user's last line was: "{last_user_line}"
        Respond with the next line of your character, keeping the scene flowing naturally.
        """

    def check_user_line_is_valid(self, user_line):
        try:
            prompt = f"The user said: '{user_line}' in the play '{self.play.title}'."
            print("prompt: ", prompt)
            return self.llm_client.check_user_line_is_valid(
                prompt=prompt, play_title=self.play.title
            )
        except Exception as e:
            print("error when setting play and user: ", e)
