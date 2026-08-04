class Move:
    """
    Represents a single checkers move.
    """

    def __init__(self, from_square, to_square):
        self.from_square = from_square
        self.to_square = to_square

    def describe(self):
        return f"Move from {self.from_square} to {self.to_square}"

    def __str__(self):
        return self.describe()