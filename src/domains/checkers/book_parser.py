from .parser import CheckersParser


class CheckersBookParser:
    """
    Converts a list of checkers moves into Move objects.
    """

    def __init__(self):
        self.parser = CheckersParser()

    def parse_book(self, text):
        moves = []

        lines = text.splitlines()

        for line in lines:
            line = line.strip()

            if line:
                move = self.parser.parse(line)

                if move:
                    moves.append(move)

        return moves