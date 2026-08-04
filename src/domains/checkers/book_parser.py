from .parser import CheckersParser
from .variation import Variation


class CheckersBookParser:
    """
    Converts checkers notation into a Variation.
    """

    def __init__(self):
        self.parser = CheckersParser()


    def parse_book(self, text, name="Imported Game"):

        moves = []

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if line:

                move = self.parser.parse(line)

                if move:
                    moves.append(move)


        return Variation(name, moves)