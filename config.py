import os

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")
OLLAMA_MODEL = "llama3"
TTS_VOICE_SPEED = 200
TTS_VOICE_VOLUME = 1.0
SYSTEM_PROMPT_VOICE = (
    "You are a voice assistant. "
    "Speak in full, clear sentences. "
    "Avoid using special characters, formatting like asterisks or Markdown, and code blocks. "
    "Only include code if explicitly asked. "
    "Respond as if you're speaking out loud to a human."
)
SYSTEM_PROMPT_CODE = (
    "You are a coding assistant. "
    "You will receive full projects with all of their files. "
    "Your job is to help the debugging and prevent me creating bugs in the future by helping me to write the program correctly. "
    "You are allowed to send code snippets with your answer."
)
TOKEN_LIMIT = 2048
