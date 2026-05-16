import ollama

from config.settings import AI_MODEL
from models.prompts import build_system_prompt
from models.language_detector import detect_language


class AIEngine:

    def __init__(self):

        self.model = AI_MODEL

    def build_messages(self, messages):

        user_message = messages[-1]["content"]

        language = detect_language(user_message)

        system_prompt = {
            "role": "system",
            "content": build_system_prompt(language)
        }

        return [system_prompt] + messages

    def stream(self, messages):

        final_messages = self.build_messages(messages)

        return ollama.chat(
            model=self.model,
            messages=final_messages,
            stream=True,
            options={
                "temperature": 0.7,
                "num_predict": 512
            }
        )

    def ask(self, messages):

        stream = self.stream(messages)

        full_response = ""

        for chunk in stream:

            content = chunk["message"]["content"]

            full_response += content

        return full_response