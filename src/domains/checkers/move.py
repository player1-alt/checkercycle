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

            path = "x".join(
                str(square)
                for square in self.path
            )

            captures = ", ".join(
                str(square)
                for square in self.captured_squares
            )

            return (
                f"{path} "
                f"(captures: {captures})"
            )


        path = "-".join(
            str(square)
            for square in self.path
        )

        return path


    def __str__(self):
        return self.describe()