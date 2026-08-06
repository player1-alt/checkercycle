class MoveEvent:
    """
    Represents everything that happens during one checker move.

    This becomes the common language between:
    - Video
    - Audio
    - Timing
    - Animation
    """

    def __init__(
        self,
        move,
        start_square,
        end_square,
        captured_squares,
        duration
    ):

        self.move = move

        # Where the piece starts
        self.start_square = start_square

        # Where the piece lands
        self.end_square = end_square

        # Any pieces removed during capture
        self.captured_squares = captured_squares

        # How long this event lasts
        self.duration = duration



    def describe(self):

        print("MOVE EVENT")
        print("----------------")

        print(
            f"Move: {self.start_square}-{self.end_square}"
        )

        if self.captured_squares:

            print(
                f"Captured: {self.captured_squares}"
            )

        else:

            print(
                "No capture"
            )

        print(
            f"Duration: {self.duration}s"
        )