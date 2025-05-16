from assistant.ai_service.ollama_service import OllamaService
from assistant.ai_service.ai_service import AIService


class AIManager:
    services: list[AIService] = [OllamaService()]

    @classmethod
    def get_installed_service(cls) -> AIService:
        for service in cls.services:
            if service.check_install():
                return service
        return cls.install_default_service()

    @classmethod
    def install_default_service(cls) -> AIService:
        service = cls.services[0]
        service.install()
        return service