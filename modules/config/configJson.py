import json
import logging
from pathlib import Path
from .default_config import default_config


class Client(object):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path.absolute()
        if not (file_path.is_file()):
            self.create_setting()
            logging.warning("Впервые создали конфиг, заполните его данными.")

    def create_setting(self):
        json_string = json.dumps(default_config, indent=4)
        Path(self.file_path.parent).mkdir(exist_ok=True, parents=True)
        with open(self.file_path, "w") as file:
            file.write(json_string)

    def get_setting(self, section, key):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        try:
            return data[section][key]
        except KeyError:
            self.set_setting(section, key, default_config[section][key])
            return default_config[section][key]

    def set_setting(self, section, key, value):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        try:
            data[section][key] = value
        except KeyError:
            data[section] = {}
            data[section][key] = value
        json_string = json.dumps(data, indent=4)
        with open(self.file_path, "w") as file:
            file.write(json_string)
