from src.renderer.timeline import Timeline
from src.renderer.audio.audio_player import AudioPlayer
from src.renderer.audio.audio_map import AUDIO_MAP
from src.renderer.settings import SETTINGS


class AudioOutput:
    """
    Converts MoveEvent information into real audio playback.

    Receives:
    - move path
    - captured squares
    - timing information

    Uses:
    - audio_map.json for square -> song assignment
    - settings.json for timing
    """


    def __init__(self):

        self.timeline = Timeline()
        self.player = AudioPlayer()



    def display(self, event):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")

        move = event.move

        files = []


        # Build audio sequence from move path

        for square in move.path:

            print(
                f"Square {square}"
            )


            if square in AUDIO_MAP:

                files.append(
                    f"assets/audio/{AUDIO_MAP[square]}"
                )

            else:

                print(
                    f"No audio assigned to square {square}"
                )



        # Play move audio

        if files:

            self.player.play_sequence(
                files,
                pause=SETTINGS["audio"]["move_hold"]
            )



        # Capture audio placeholder

        if event.captured_squares:

            print(
                "Capture audio:"
            )


            for square in event.captured_squares:

                print(
                    f"Capture Square {square}"
                )


        print()