class AudioOutput:
    """
    Converts renderer information into audio instructions.
    """

    def display(self, move):

        print("AUDIO OUTPUT:")
        print("Preparing audio:")

        for square in move.path:

            print(
                f"Square {square}.mp3"
            )

        print()