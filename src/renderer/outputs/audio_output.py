from src.renderer.timeline import Timeline


class AudioOutput:
    """
    Converts MoveEvent information into audio instructions.

    Later this will control real MP3 playback.
    """


    def __init__(self):

        self.timeline = Timeline()



    def display(self, event):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")


        # Full movement path
        path = event.move.path



        for index, square in enumerate(path):

            print(
                f"Playing Square {square}.mp3"
            )


            # Pause between squares

            if index < len(path) - 1:

                hold = self.timeline.hold_time(
                    index + 1,
                    len(path)
                )


                print(
                    f"Hold {hold}s"
                )



        # Capture information

        if event.captured_squares:

            print()

            print("Capture audio:")

            for square in event.captured_squares:

                print(
                    f"Captured Square {square}.mp3"
                )



        print()