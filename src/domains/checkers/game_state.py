from src.renderer.pieces import Pieces
from src.domains.checkers.square_mapper import SquareMapper


class GameState:

    def __init__(self):
        self.pieces = Pieces()
        self.square_mapper = SquareMapper()

    # ==========================
    # FIND CAPTURED SQUARES
    # ==========================

    def find_captured_squares(
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

        row_difference = to_row - from_row
        col_difference = to_col - from_col

        row_distance = abs(row_difference)
        col_distance = abs(col_difference)

        print(f"ROW DIFFERENCE: {row_difference}")
        print(f"COL DIFFERENCE: {col_difference}")

        # A checkers move must travel diagonally.
        if row_distance != col_distance:
            print("NOT A DIAGONAL MOVE")
            print("===================================")
            print()

            return []

        if row_distance < 2:
            print("NOT A CAPTURE")
            print("===================================")
            print()

            return []

        row_step = 1 if row_difference > 0 else -1
        col_step = 1 if col_difference > 0 else -1

        captured_squares = []

        current_row = from_row + row_step
        current_col = from_col + col_step

        while (
            current_row != to_row
            and current_col != to_col
        ):

            square = self.square_mapper.square(
                current_row,
                current_col
            )

            piece = self.pieces.piece_at(square)

            if piece is not None:

                captured_squares.append(square)

                print(
                    f"CAPTURE CANDIDATE: "
                    f"{square}"
                )

            current_row += row_step
            current_col += col_step

        print(
            f"CAPTURED SQUARES: "
            f"{captured_squares}"
        )

        print("===================================")
        print()

        return captured_squares

    # ==========================
    # APPLY MOVE
    # ==========================

    def apply_move(self, move):

        piece = self.pieces.piece_at(
            move.from_square
        )

        # If the parser already supplied
        # capture information, preserve it.
        #
        # Otherwise determine captures
        # automatically from the board.

        if not move.captured_squares:

            captured_squares = self.find_captured_squares(
                move.from_square,
                move.to_square
            )

            if captured_squares:

                print(
                    "Automatically detected captures:",
                    captured_squares
                )

                move.captured_squares.extend(
                    captured_squares
                )

        print(
            f"Final captured squares: "
            f"{move.captured_squares}"
        )

        # Remove moving piece from origin.
        self.pieces.position[
            move.from_square
        ] = None

        # Remove every captured piece.
        for square in move.captured_squares:

            print(
                f"Removing piece from square {square}"
            )

            self.pieces.position[
                square
            ] = None

        # Put moving piece on destination.
        self.pieces.position[
            move.to_square
        ] = piece

        self.check_promotion(
            piece,
            move.to_square
        )

    # ==========================
    # PROMOTION
    # ==========================

    def check_promotion(
        self,
        piece,
        square
    ):

        red_king_row = [
            29,
            30,
            31,
            32
        ]

        white_king_row = [
            1,
            2,
            3,
            4
        ]

        if piece.color == "red":

            if square in red_king_row:
                piece.promote()

        elif piece.color == "white":

            if square in white_king_row:
                piece.promote()