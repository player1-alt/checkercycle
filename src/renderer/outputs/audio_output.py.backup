from src.renderer.audio.audio_map import AUDIO_MAP
from pydub import AudioSegment
import os


class AudioOutput:
    """
    Builds MP3 audio timeline from MoveEvents.

    Uses:
    - audio_map.json
    - MoveEvent timing
    - square -> song memory palace
    """


    def __init__(self):

        self.audio_track = AudioSegment.empty()

        self.base_path = "assets/audio"



    def add_event(self, event):

        move = event.move


        print()
        print("AUDIO EVENT")
        print("----------------")


        for square in move.path:


            print(
                f"Square {square}"
            )


            if square in AUDIO_MAP:


                filename = AUDIO_MAP[square]


                filepath = os.path.join(
                    self.base_path,
                    filename
                )


                if os.path.exists(filepath):


                    print(
                        "Adding:",
                        filepath
                    )


                    sound = AudioSegment.from_mp3(
                        filepath
                    )


                    # Match video timing

                    duration = (
                        event.duration
                        +
                        event.hold_time
                    ) * 1000


                    sound = sound[:duration]


                    self.audio_track += sound


                else:

                    print(
                        "Missing audio:",
                        filepath
                    )


            else:

                print(
                    "No song assigned:",
                    square
                )



    def save(self):

        filename = "CheckerCycle_audio.mp3"


        self.audio_track.export(
            filename,
            format="mp3"
        )


        print()
        print("=====================")
        print(
            "AUDIO OUTPUT:",
            filename
        )
        print("=====================")