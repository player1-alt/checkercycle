class AudioOutput:
    """
    Converts renderer information into audio instructions.
    """

    def display(self, data):
        print("AUDIO OUTPUT:")
        print("Preparing audio:")
        print(f"Square {data.from_square}.mp3")
        print(f"Square {data.to_square}.mp3")