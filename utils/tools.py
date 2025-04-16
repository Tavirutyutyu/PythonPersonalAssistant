import json
import os


def load(file_name:str, base_path:str) -> dict:
    file_path = os.path.join(base_path, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
