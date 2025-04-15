import json
import os

from config import RESOURCES_DIR


def load(file_name:str, base_path:str) -> dict:
    file_path = os.path.join(base_path, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

command_metadata = load("launch_ide_command.json", RESOURCES_DIR)
print(command_metadata["keywords"])
print(command_metadata["sub_options"])