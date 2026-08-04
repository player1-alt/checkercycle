class Move:
    """
    Represents a single checkers move or capture sequence.
    """

    def __init__(
        self,
        path,
        is_capture=False,
        captured_squares=None
    ):

        self.path = path

        self.is_capture = is_capture

        if captured_squares is None:
            self.captured_squares = []
        else:
            self.captured_squares = captured_squares


    @property
    def from_square(self):
        return self.path[0]


    @property
    def to_square(self):
        return self.path[-1]


    def describe(self):

        if self.is_capture:
            return (
                f"Capture {self.path} "
                f"removed {self.captured_squares}"
            )

        return (
            f"Move from {self.from_square} "
            f"to {self.to_square}"
        )


    def __str__(self):
        return self.describe()