from src.renderer.pieces import Pieces
from src.domains.checkers.square_mapper import SquareMapper


class GameState:

    def __init__(self):
        self.pieces = Pieces()
        self.square_mapper = SquareMapper()


    def find_captured_square(
        self,
        from_square,
        to_square
    ):

        from_row, from_col = self.square_mapper.coordinates(
            from_square
        )

        to_row, to_col = self.square_mapper.coordinates(
            to_square
        )

        print()
        print("========== CAPTURE DEBUG ==========")
        print(f"FROM: {from_square} -> ({from_row}, {from_col})")
        print(f"TO:   {to_square} -> ({to_row}, {to_col})")

        row_difference = abs(
            from_row - to_row
        )

        col_difference = abs(
            from_col - to_col
        )

        print(f"ROW DIFFERENCE: {row_difference}")
        print(f"COL DIFFERENCE: {col_difference}")

        if row_difference != 2 or col_difference != 2:

            print("NOT A CAPTURE")
            print("===================================")
            print()

            return None

        middle_row = (
            from_row + to_row
        ) // 2

        middle_col = (
            from_col + to_col
        ) // 2

        captured_square = self.square_mapper.square(
            middle_row,
            middle_col
        )

        print(f"MIDDLE: ({middle_row}, {middle_col})")
        print(f"CAPTURED SQUARE: {captured_square}")
        print("===================================")
        print()

        return captured_square


    def apply_move(self, move):

        piece = self.pieces.piece_at(
            move.from_square
        )

        if not move.captured_squares:

            captured = self.find_captured_square(
                move.from_square,
                move.to_square
            )

            if captured is not None:

                print(f"Automatically detected capture: {captured}")

                move.captured_squares.append(
                    captured
                )

        print(f"Final captured squares: {move.captured_squares}")

        self.pieces.position[
            move.from_square
        ] = None

        for square in move.captured_squares:

            print(f"Removing piece from square {square}")

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


    def check_promotion(
        self,
        piece,
        square
    ):

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