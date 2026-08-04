from src.renderer.pieces import Pieces


class GameState:

    def __init__(self):
        self.pieces = Pieces()


    def apply_move(self, move):

        # Get moving piece
        piece = self.pieces.piece_at(
            move.from_square
        )

        # Remove piece from starting square
        self.pieces.position[
            move.from_square
        ] = None


        # Remove captured pieces
        for square in move.captured_squares:

            self.pieces.position[square] = None


        # Place piece at destination
        self.pieces.position[
            move.to_square
        ] = piece