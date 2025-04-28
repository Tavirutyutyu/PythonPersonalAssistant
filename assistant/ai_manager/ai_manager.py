from .ollama_manager import OllamaManager
from .local_ai_manager_base import  LocalAIManagerBase


class AIManager:
    def __init__(self):
        self.__ai_managers = [OllamaManager()]
        self.__installed_manager: LocalAIManagerBase = self.__check_install()

    def __check_install(self):
        manager = None
        for ai_manager in self.__ai_managers:
            if ai_manager.check_install():
                manager = ai_manager
        if manager is None:
            manager = self.__install_default()
        return manager

    def __install_default(self):
        manager = self.__ai_managers[0]
        manager.install()
        return manager

    def get_installed_manager(self):
        return self.__installed_manager
