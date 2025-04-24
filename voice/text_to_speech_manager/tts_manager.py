from voice.text_to_speech_handler import TextToSpeechBase
from voice.text_to_speech_manager import FestivalManager
from voice.text_to_speech_manager import TTSManagerBase


class TextToSpeechManager:
    def __init__(self):
        self.__tts_managers = [FestivalManager()]
        self.__installed_manager: TTSManagerBase = self.__check_install()

    def __check_install(self) -> TTSManagerBase:
        manager = None
        for tts_manager in self.__tts_managers:
            if tts_manager.check_install():
                manager = tts_manager
        if manager is None:
            manager = self.__install_default()
        return manager

    def __install_default(self) -> TTSManagerBase:
        manager = self.__tts_managers[0]
        manager.install()
        return manager

    def get_tts_model(self) -> TextToSpeechBase:
        if self.__installed_manager:
            return self.__installed_manager.get_tts_model()
        else:
            manager = self.__install_default()
            return manager.get_tts_model()