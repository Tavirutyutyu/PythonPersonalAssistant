import openai

from assistant.ai_handler import AIHandler
from config import GPT_MODEL


class GPTHandler(AIHandler):
    def __init__(self, model:str = None):
        super().__init__(model or GPT_MODEL)

    def generate_response(self, prompt:str):
        self._message_history.append({"role": "user", "content": prompt})
        try:
            response = openai.ChatCompletion.create(
                model=self._model,
                messages=self._message_history,
            )
            reply = response.choices[0].message["content"]
            self._message_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Something went wrong while contacting GPT: {e}"