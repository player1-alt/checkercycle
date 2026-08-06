from src.renderer.timeline import Timeline


class AudioOutput:
    """
    Converts MoveEvent information into audio instructions.

    Later this will control real MP3 playback.

    Receives:
    - start square
    - end square
    - timing
    - captures
    """


    def __init__(self):

        self.timeline = Timeline()



    def display(self, event):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")

        move = event.move


        for index, square in enumerate(
            move.path
        ):


            print(
                f"Playing Square {square}.mp3"
            )


            # Pause between squares

            if index < len(move.path) - 1:


                hold = self.timeline.hold_time(
                    index + 1,
                    len(move.path)
                )


                print(
                    f"Hold {hold}s"
                )



        # Capture sound placeholder

        if event.captured_squares:

            print(
                "Capture audio:"
            )


            for square in event.captured_squares:

                print(
                    f"Capture Square {square}.mp3"
                )


        print()