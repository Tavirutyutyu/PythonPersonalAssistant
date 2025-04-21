import platform
import shutil
import subprocess
import time
from os import setsid, killpg, getpgid
from signal import SIGTERM
from subprocess import Popen, DEVNULL

from assistant.ai_manager.local_ai_manager import LocalAIManager
from config import ARCH_BASED, DEBIAN_BASED, REDHAT_BASED, SUSE_BASED


class OllamaManager(LocalAIManager):
    def __init__(self):
        super().__init__()

    def __check_install(self):
        if shutil.which("ollama") is None:
            return False
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if result.returncode != 0:
                return False
            return "MODEL NAME" in result.stdout or len(result.stdout.strip().splitlines()) > 1
        except Exception as e:
            print(f"{e.__class__.__name__} - Error: {e}")
            return False

    def __install(self):
        system = platform.system()
        if system == "Darwin":
            self.__install_mac()
        elif system == "Linux":
            self.__install_linux()
        elif system == "Windows":
            self.__install_windows()

    def _start_server(self):
        if self._process is None:
            self._process = Popen(
                ["ollama", "serve"],
                stdout=DEVNULL,
                stderr=DEVNULL,
                preexec_fn=setsid,
            )
            time.sleep(1.5)

    def stop_server(self):
        if self._process is not None:
            killpg(getpgid(self._process.pid), SIGTERM)
            self._process = None

    def __install_linux(self):
        linux_distro = self.__get_linux_distro()
        if linux_distro:
            if ARCH_BASED in linux_distro:
                self.__install_arch()
            elif DEBIAN_BASED in linux_distro:
                self.__install_debian()
            elif REDHAT_BASED in linux_distro:
                self.__install_redhat()
            elif SUSE_BASED in linux_distro:
                self.__install_suse()

    @staticmethod
    def __install_arch():
        if shutil.which("yay"):
            subprocess.run(["yay", "-S", "--noconfirm", "ollama-bin"])
            try:
                subprocess.run(["ollama", "pull", "llama3"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to pull the default model. Reason: {e}")

    @staticmethod
    def __install_debian():
        pass

    @staticmethod
    def __install_redhat():
        pass

    @staticmethod
    def __install_suse():
        pass

    @staticmethod
    def __install_windows():
        pass

    @staticmethod
    def __install_mac():
        subprocess.run(["brew", "install", "ollama"])

    @staticmethod
    def __get_linux_distro():
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.strip().split("=")[1].strip('"').lower()
        except Exception as e:
            print(f"Could not get linux distro:\nError Type: {e.__class__.__name__}\nError: {e}")
