from src.renderer.pieces import Pieces
from src.domains.checkers.piece import Piece


class KingTest:

    def create_position(self):

        pieces = Pieces()


        # Clear board

        for square in pieces.position:

            pieces.position[square] = None


        # Put red piece on king row

        pieces.position[29] = Piece(
            "red"
        )


        # Manual promotion test

        pieces.position[29].king = True


        return pieces