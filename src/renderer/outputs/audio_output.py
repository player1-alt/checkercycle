from src.renderer.timeline import Timeline


class AudioOutput:
    """
    Converts renderer information into audio instructions.

    Later this will control real MP3 playback.
    """

    def __init__(self):

        self.timeline = Timeline()


    def display(self, move):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")

        path = move.path


        for index, square in enumerate(path):

            print(
                f"Playing Square {square}.mp3"
            )


            # Add a pause between squares
            if index < len(path) - 1:

                hold = self.timeline.hold_time(
                    index + 1,
                    len(path)
                )

                print(
                    f"Hold {hold}s"
                )


        print()