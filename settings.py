"""
Reading and writing settings of the game into the settings.json file
"""
import json
import sys
from pathlib import Path

class Settings:
    def __init__(self, settings_path: str = "settings.json"):
        self.path = Path(settings_path)
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("settings.json was not found")
            sys.exit(1)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

settings = Settings()
