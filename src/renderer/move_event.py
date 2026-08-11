
class MoveEvent:
    """
    Represents everything that happens during one checker move.

    Timing for each square:
    - audio_duration = 10 seconds
    - move_pause = 3 seconds
    - total_duration = 13 seconds
    """

    def __init__(
        self,
        move,
        start_square,
        end_square,
        captured_squares,
        audio_duration,
        move_pause,
        moving_piece
    ):

        self.move = move

        self.start_square = start_square

        self.end_square = end_square

        self.captured_squares = captured_squares

        self.audio_duration = audio_duration

        self.move_pause = move_pause

        self.total_duration = (
            audio_duration
            + move_pause
        )

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
            f"Audio duration: {self.audio_duration}s"
        )

        print(
            f"Move pause: {self.move_pause}s"
        )

        print(
            f"Total square duration: {self.total_duration}s"
        )
