class Variation:
    """
    Represents a sequence of checkers moves.
    """

    def __init__(self, name, moves):
        self.name = name
        self.moves = moves

    def describe(self):
        return f"{self.name}: {len(self.moves)} moves"