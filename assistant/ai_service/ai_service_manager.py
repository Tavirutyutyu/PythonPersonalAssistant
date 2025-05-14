from assistant.ai_service.ollama_service import OllamaService
from assistant.ai_service.ai_service import AIService


class AIServiceManager:
    services: list[AIService] = [OllamaService()]

    @staticmethod
    def get_installed_service() -> AIService | None:
        for service in AIServiceManager.services:
            if service.check_install():
                return service
        return AIServiceManager.install_default_service()

    @staticmethod
    def install_default_service():
        service = AIServiceManager.services[0]
        service.install()
        return service