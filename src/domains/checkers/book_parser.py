from .parser import CheckersParser
from .variation import Variation


class CheckersBookParser:
    """
    Converts checkers notation into a Variation.

    Supports:
    11-15
    23x16x7|19,11
    1. 11-15
    2. 23-19

    Also supports multiple moves on one line:
    11-15 23-19 9-13 22-18
    """

    def __init__(self):
        self.parser = CheckersParser()

    def parse_book(self, text, name="Imported Game"):

        moves = []

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Remove move numbers
            if "." in line:
                line = line.split(".", 1)[1].strip()

            # Allow multiple moves on one line
            tokens = line.split()

            for token in tokens:

                move = self.parser.parse(token)

                if move:
                    moves.append(move)

        return Variation(name, moves)