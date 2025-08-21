from . import FestivalService
from . import TtsService
from .pytts3_service import Pytts3Service


class TtsManager:
    services: list[TtsService] = [Pytts3Service(), FestivalService()]

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
