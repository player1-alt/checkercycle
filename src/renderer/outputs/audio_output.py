
from src.renderer.audio.audio_map import AUDIO_MAP
from pydub import AudioSegment
import os


class AudioOutput:
    """
    Builds the CheckerCycle MP3 timeline.

    For every square:

        10 seconds of that square's MP3
        3 seconds of silence

    Every MP3 segment starts from 0:00.
    """

    def __init__(self):

        self.audio_track = AudioSegment.empty()

        self.base_path = "assets/audio"

        self.audio_duration = 10.0
        self.move_pause = 3.0

    def add_event(self, event):

        move = event.move

        print()
        print("AUDIO EVENT")
        print("----------------")

        for square in move.path:

            print(
                f"Square {square}"
            )

            if square not in AUDIO_MAP:

                print(
                    "No song assigned:",
                    square
                )

                continue

            filename = AUDIO_MAP[square]

            filepath = os.path.join(
                self.base_path,
                filename
            )

            if not os.path.exists(filepath):

                print(
                    "Missing audio:",
                    filepath
                )

                continue

            print(
                "Adding:",
                filepath
            )

            try:

                sound = AudioSegment.from_mp3(
                    filepath
                )

                # Always take audio from 0:00.
                sound = sound[:int(
                    self.audio_duration * 1000
                )]

                self.audio_track += sound

                # Exactly 3 seconds of silence
                # after each square.
                self.audio_track += AudioSegment.silent(
                    duration=int(
                        self.move_pause * 1000
                    )
                )

            except Exception as e:

                print(
                    "Audio processing error:",
                    e
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
