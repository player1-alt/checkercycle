import json


CONFIG_FILE = "config/settings.json"


def load_settings():

    with open(CONFIG_FILE, "r") as file:

        return json.load(file)


SETTINGS = load_settings()