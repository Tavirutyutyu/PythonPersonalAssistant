import requests
from config import OLLAMA_MODEL, OLLAMA_URL, SYSTEM_PROMPT_VOICE, SYSTEM_PROMPT_CODE
from .ai_handler import AIHandler
import ollama

class OllamaHandler(AIHandler):
    def __init__(self, model: str = OLLAMA_MODEL):
        super().__init__(model)
        self.url = OLLAMA_URL

    def generate_response(self, prompt: str, mode: str = "assistant", root_directory: str | None = None, entry_point: str | None = None, uploaded_file_paths: list | None = None) -> str:
        self._message_history.append(dict(role="user", content=prompt))
        try:
            response = ollama.chat(model=OLLAMA_MODEL, messages=self._message_history)
            return response.message.content
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")
       
    def _format_prompt(self, messages: list[dict], mode: str = "assistant", root_directory:str|None=None, entry_point:str | None = None, uploaded_file_paths:list | None = None) -> str:
        """Turn message history into a plain text prompt Ollama understands."""
        prompt = ""
        if mode == "assistant":
            prompt = f"System: {SYSTEM_PROMPT_VOICE}\n"
        elif mode == "code":
            prompt = f"System: {SYSTEM_PROMPT_CODE}\n"
            full_project_content = self.__def_combined_files(uploaded_file_paths)
            print(full_project_content)
            prompt += full_project_content
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        return prompt

    
