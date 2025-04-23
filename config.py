import os

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"
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
)

