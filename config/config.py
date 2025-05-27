import json
import os

from config import SYSTEM_PROMPT_VOICE_ENGLISH, SYSTEM_PROMPT_CODE_ENGLISH, SYSTEM_PROMPT_VOICE_HUNGARIAN, SYSTEM_PROMPT_CODE_HUNGARIAN


class Configuration:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCES_DIR = os.path.join(PROJECT_ROOT, "resources")
    OLLAMA_MODEL = "llama3"
    TOKEN_LIMIT = 2048

    TTS = {
        "voice_speed": 1.0,
        "voice_model": "kal_diphone",
    }

    USER_INPUT_LANGUAGES = ["english", "hungarian"]
    SYSTEM_OUTPUT_LANGUAGES = ["english", "hungarian"]

    SYSTEM_PROMPTS = {
        "english": {
            "voice": SYSTEM_PROMPT_VOICE_ENGLISH,
            "code": SYSTEM_PROMPT_CODE_ENGLISH,
        },
        "hungarian": {
            "voice": SYSTEM_PROMPT_VOICE_HUNGARIAN,
            "code": SYSTEM_PROMPT_CODE_HUNGARIAN,
        }
    }

    SETTINGS_FILE = os.path.join(RESOURCES_DIR, "settings.json")

    active_language = "english"

    _font_size = 12
    _observers = {}

    @classmethod
    def set_font_size(cls, size: int):
        cls._font_size = size
        cls._notify("font_size", size)

    @classmethod
    def get_font_size(cls):
        return cls._font_size

    @classmethod
    def on_change(cls, key:str, callback):
        if key not in cls._observers:
            cls._observers[key] = []
        cls._observers[key].append(callback)

    @classmethod
    def _notify(cls, key: str, value):
        for callback in cls._observers.get(key, []):
            callback(value)

    @classmethod
    def get_system_prompt(cls, mode):
        return cls.SYSTEM_PROMPTS[cls.active_language][mode]

    @classmethod
    def set_language(cls, lang: str):
        if lang in cls.USER_INPUT_LANGUAGES:
            cls.active_language = lang
        else:
            raise ValueError(f"Language '{lang}' is not supported.")

    @classmethod
    def update_tts(cls, speed:float | None = None, voice:str | None = None):
        if speed:
            cls.TTS["voice_speed"] = speed
        if voice:
            cls.TTS["voice_model"] = voice

    @classmethod
    def save(cls):
        data = {
            "OLLAMA_MODEL": cls.OLLAMA_MODEL,
            "TOKEN_LIMIT": cls.TOKEN_LIMIT,
            "TTS": cls.TTS,
            "USER_INPUT_LANGUAGES": cls.USER_INPUT_LANGUAGES,
            "SYSTEM_OUTPUT_LANGUAGES": cls.SYSTEM_OUTPUT_LANGUAGES,
            "ACTIVE_LANGUAGE": cls.active_language
        }
        with open(cls.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls):
        try:
            with open(cls.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls.OLLAMA_MODEL = data.get("OLLAMA_MODEL", cls.OLLAMA_MODEL)
                cls.TOKEN_LIMIT = data.get("TOKEN_LIMIT", cls.TOKEN_LIMIT)
                cls.TTS = data.get("TTS", cls.TTS)
                cls.USER_INPUT_LANGUAGES = data.get("USER_INPUT_LANGUAGES", cls.USER_INPUT_LANGUAGES)
                cls.SYSTEM_OUTPUT_LANGUAGES = data.get("SYSTEM_OUTPUT_LANGUAGES", cls.SYSTEM_OUTPUT_LANGUAGES)
                cls.active_language = data.get("ACTIVE_LANGUAGE", cls.active_language)
        except FileNotFoundError:
            cls.save()