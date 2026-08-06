from src.renderer.audio.audio_player import AudioPlayer
from src.renderer.audio.audio_map import AUDIO_MAP


class AudioOutput:
    """
    Converts MoveEvent information into real audio playback.

    Receives:
    - move path
    - captured squares
    - duration
    - hold time

    Uses:
    - audio_map.json for square -> song assignment
    - MoveEvent as timing authority
    """


    def __init__(self):

        self.player = AudioPlayer()



    def display(self, event):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")


        move = event.move

        files = []


        # Build audio sequence

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



        # Playback follows MoveEvent timing

        if files:

            self.player.play_sequence(
                files,
                move_time=event.duration,
                hold_time=event.hold_time
            )



        # Capture sound placeholder

        if event.captured_squares:

            print(
                "Capture audio:"
            )


            for square in event.captured_squares:

                print(
                    f"Capture Square {square}"
                )


        print()