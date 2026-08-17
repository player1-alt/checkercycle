import json
import os


CONFIG_FILE = "config/settings.json"


def load_settings():

    if not os.path.exists(
        CONFIG_FILE
    ):

        return {
            "timing": {
                "mode_13": 13.0,
                "mode_8": 8.0,
                "mode_4": 4.0,
                "transition": 1.0
            }
        }


    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        settings = json.load(file)


    if "timing" not in settings:

        settings["timing"] = {}


    if "mode_13" not in settings["timing"]:

        settings["timing"]["mode_13"] = 13.0


    if "mode_8" not in settings["timing"]:

        settings["timing"]["mode_8"] = 8.0


    if "mode_4" not in settings["timing"]:

        settings["timing"]["mode_4"] = 4.0


    if "transition" not in settings["timing"]:

        settings["timing"]["transition"] = 1.0


    return settings


SETTINGS = load_settings()