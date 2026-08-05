from src.renderer.pieces import Pieces


class GameState:

    def __init__(self):
        self.pieces = Pieces()


    def apply_move(self, move):

        piece = self.pieces.piece_at(
            move.from_square
        )

        self.pieces.position[
            move.from_square
        ] = None


        for square in move.captured_squares:

            self.pieces.position[
                square
            ] = None


        self.pieces.position[
            move.to_square
        ] = piece


        self.check_promotion(
            piece,
            move.to_square
        )


    def check_promotion(self, piece, square):

        red_king_row = [
            29, 30, 31, 32
        ]

        white_king_row = [
            1, 2, 3, 4
        ]


        if piece.color == "red":

            if square in red_king_row:
                piece.promote()


        elif piece.color == "white":

            if square in white_king_row:
                piece.promote()