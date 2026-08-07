from src.renderer.audio.audio_map import AUDIO_MAP
import os
import json


class AudioOutput:
    """
    Builds audio timeline instructions.

    Final audio rendering will use FFmpeg.

    Uses:
    - audio_map.json
    - move timing
    - square assignments
    """


    def __init__(self):

        self.events = []



    def add_event(self, move):

        print()
        print("AUDIO EVENT")
        print("----------------")


        for square in move.path:


            if square in AUDIO_MAP:

                filename = AUDIO_MAP[square]


                filepath = os.path.join(
                    "assets",
                    "audio",
                    filename
                )


                print(
                    "Square",
                    square,
                    "->",
                    filepath
                )


                self.events.append(
                    {
                        "square": square,
                        "file": filepath
                    }
                )


            else:

                print(
                    "No song assigned:",
                    square
                )



    def save(self):

        filename = "audio_timeline.json"


        with open(
            filename,
            "w"
        ) as file:

            json.dump(
                self.events,
                file,
                indent=4
            )


        print()
        print("=====================")
        print(
            "AUDIO TIMELINE:",
            filename
        )
        print("=====================")