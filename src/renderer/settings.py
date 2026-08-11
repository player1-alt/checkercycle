
import json
import os


CONFIG_FILE = "config/settings.json"


def load_settings():

    if not os.path.exists(
        CONFIG_FILE
    ):

        return {
            "audio": {
                "square_duration": 10.0,
                "move_pause": 3.0
            },
            "video": {
                "final_hold": 5.0
            }
        }


    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        settings = json.load(file)


    if "audio" not in settings:

        settings["audio"] = {}


    if "square_duration" not in settings["audio"]:

        settings["audio"]["square_duration"] = 10.0


    if "move_pause" not in settings["audio"]:

        settings["audio"]["move_pause"] = 3.0


    if "video" not in settings:

        settings["video"] = {}


    if "final_hold" not in settings["video"]:

        settings["video"]["final_hold"] = 5.0


    return settings


SETTINGS = load_settings()
