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
        hold_time,
        moving_piece
    ):

        self.move = move

        self.start_square = start_square

        self.end_square = end_square

        self.captured_squares = captured_squares

        self.duration = duration

        self.hold_time = hold_time

        # Snapshot of piece before board changes
        self.moving_piece = moving_piece



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
            print("No capture")

        print(
            f"Move duration: {self.duration}s"
        )

        print(
            f"Study hold: {self.hold_time}s"
        )