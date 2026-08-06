class MoveEvent:
    """
    Represents everything that happens during one checker move.

    Communication layer between:
    - Animation
    - Audio
    - Timing
    - Video
    """

    def __init__(
        self,
        move,
        start_square,
        end_square,
        captured_squares,
        duration,
        hold_time
    ):

        # Original move object
        self.move = move

        # Starting square
        self.start_square = start_square

        # Ending square
        self.end_square = end_square

        # Pieces removed during capture
        self.captured_squares = captured_squares

        # Time used for piece movement animation
        self.duration = duration

        # Time used for studying the new position
        self.hold_time = hold_time



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
            f"Move duration: {self.duration}s"
        )

        print(
            f"Study hold: {self.hold_time}s"
        )