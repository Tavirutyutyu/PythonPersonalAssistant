from voice.tts_service.festival_service import FestivalService
from random import choice

festival_service = FestivalService()
voices = festival_service.get_festival_voices()
festival_service.set_voice_property(voice=choice(voices), speed=1.2)
festival_service.say("Hello there!")
