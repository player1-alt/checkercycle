import json


CONFIG_FILE = "config/audio_map.json"


def load_audio_map():

    with open(CONFIG_FILE, "r") as file:

        data = json.load(file)

    return {
        int(square): song
        for square, song in data.items()
        if song
    }


AUDIO_MAP = load_audio_map()