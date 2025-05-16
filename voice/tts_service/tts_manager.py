from . import FestivalService
from . import TtsService


class TtsManager:
    services: list[TtsService] = [FestivalService()]

    @classmethod
    def get_installed_service(cls) -> TtsService:
        for service in TtsManager.services:
            if service.check_install():
                return service
        return cls.install_default_service()

    @classmethod
    def install_default_service(cls) -> TtsService:
        service = cls.services[0]
        service.install()
        return service
