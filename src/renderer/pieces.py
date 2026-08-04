from src.domains.checkers.piece import Piece


class Pieces:

    def __init__(self):

        self.position = {}

        # Black (Red in the renderer later)
        for square in range(1, 13):
            self.position[square] = Piece("red")

        # Empty playable squares
        for square in range(13, 21):
            self.position[square] = None

        # White
        for square in range(21, 33):
            self.position[square] = Piece("white")

    def piece_at(self, square):

        return self.position[square]