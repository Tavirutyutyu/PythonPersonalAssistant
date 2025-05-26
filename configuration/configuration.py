import json
import os

from configuration import SYSTEM_PROMPT_VOICE_ENGLISH, SYSTEM_PROMPT_CODE_ENGLISH, SYSTEM_PROMPT_VOICE_HUNGARIAN, SYSTEM_PROMPT_CODE_HUNGARIAN
from voice.tts_service import FestivalService


class Configuration:
    RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")
    OLLAMA_MODEL = "llama3"
    TOKEN_LIMIT = 2048

    TTS = {
        "voice_speed": 200,
        "voice_model": FestivalService.get_festival_voices()[0],
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

    ACTIVE_LANGUAGE = "english"

    @classmethod
    def get_system_prompt(cls, mode):
        return cls.SYSTEM_PROMPTS[cls.ACTIVE_LANGUAGE][mode]

    @classmethod
    def set_language(cls, lang: str):
        if lang in cls.USER_INPUT_LANGUAGES:
            cls.ACTIVE_LANGUAGE = lang
        else:
            raise ValueError(f"Language '{lang}' is not supported.")

    @classmethod
    def update_tts(cls, speed:int | None, voice:str | None):
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
            "ACTIVE_LANGUAGE": cls.ACTIVE_LANGUAGE
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
                cls.ACTIVE_LANGUAGE = data.get("ACTIVE_LANGUAGE", cls.ACTIVE_LANGUAGE)
        except FileNotFoundError:
            cls.save()