from src.renderer.pieces import Pieces
from src.domains.checkers.square_mapper import SquareMapper


class GameState:

    def __init__(self):

        self.pieces = Pieces()
        self.square_mapper = SquareMapper()

    # ==========================
    # AUTOMATIC MULTI-JUMP FINDER
    # ==========================

    def find_jump_path(
        self,
        from_square,
        to_square,
        piece
    ):

        start = self.square_mapper.coordinates(
            from_square
        )

        target = self.square_mapper.coordinates(
            to_square
        )

        # Copy the current board so the search
        # can simulate jumps without changing
        # the real game state.

        board = dict(
            self.pieces.position
        )

        # Remove the moving piece from its
        # starting square during the search.

        board[from_square] = None

        path = [from_square]
        captured = []

        result = self._search_jump_path(
            current_square=from_square,
            target_coordinates=target,
            piece=piece,
            board=board,
            path=path,
            captured=captured
        )

        return result

    # ==========================
    # RECURSIVE JUMP SEARCH
    # ==========================

    def _search_jump_path(
        self,
        current_square,
        target_coordinates,
        piece,
        board,
        path,
        captured
    ):

        current_row, current_col = (
            self.square_mapper.coordinates(
                current_square
            )
        )

        target_row, target_col = (
            target_coordinates
        )

        # We have reached the requested
        # destination.

        if (
            current_row == target_row
            and current_col == target_col
        ):

            if len(path) > 1:

                return (
                    list(path),
                    list(captured)
                )

            return None

        directions = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        for row_direction, col_direction in directions:

            middle_row = (
                current_row
                + row_direction
            )

            middle_col = (
                current_col
                + col_direction
            )

            landing_row = (
                current_row
                + (row_direction * 2)
            )

            landing_col = (
                current_col
                + (col_direction * 2)
            )

            # Make sure the landing square is
            # on the playable board.

            if not self._valid_coordinates(
                landing_row,
                landing_col
            ):

                continue

            try:

                middle_square = (
                    self.square_mapper.square(
                        middle_row,
                        middle_col
                    )
                )

                landing_square = (
                    self.square_mapper.square(
                        landing_row,
                        landing_col
                    )
                )

            except KeyError:

                continue

            middle_piece = board.get(
                middle_square
            )

            landing_piece = board.get(
                landing_square
            )

            # There must be an opponent piece
            # on the jumped square.

            if middle_piece is None:
                continue

            if middle_piece.color == piece.color:
                continue

            # Landing square must be empty.

            if landing_piece is not None:
                continue

            # Don't capture the same piece twice.

            if middle_square in captured:
                continue

            # Simulate this jump.

            board[current_square] = None
            board[middle_square] = None
            board[landing_square] = piece

            path.append(
                landing_square
            )

            captured.append(
                middle_square
            )

            result = self._search_jump_path(
                current_square=landing_square,
                target_coordinates=target_coordinates,
                piece=piece,
                board=board,
                path=path,
                captured=captured
            )

            if result is not None:
                return result

            # Undo simulated jump.

            board[landing_square] = None
            board[middle_square] = middle_piece
            board[current_square] = piece

            path.pop()
            captured.pop()

        return None

    # ==========================
    # BOARD COORDINATE CHECK
    # ==========================

    def _valid_coordinates(
        self,
        row,
        column
    ):

        return (
            0 <= row <= 7
            and 0 <= column <= 7
        )

    # ==========================
    # APPLY MOVE
    # ==========================

    def apply_move(
        self,
        move
    ):

        piece = self.pieces.piece_at(
            move.from_square
        )

        # -------------------------------------------------
        # AUTOMATICALLY DISCOVER A MULTI-JUMP
        #
        # Example:
        #
        #     27-11
        #
        # becomes internally:
        #
        #     27 -> 18 -> 11
        #
        # with captures:
        #
        #     23, 15
        # -------------------------------------------------

        if (
            not move.is_capture
            and not move.captured_squares
            and len(move.path) == 2
        ):

            result = self.find_jump_path(
                move.from_square,
                move.to_square,
                piece
            )

            if result is not None:

                discovered_path, discovered_captures = (
                    result
                )

                move.path = discovered_path

                move.captured_squares = (
                    discovered_captures
                )

                move.is_capture = True

                print()
                print(
                    "AUTOMATIC MULTI-JUMP DETECTED"
                )

                print(
                    f"Path: {move.path}"
                )

                print(
                    f"Captured: "
                    f"{move.captured_squares}"
                )

                print()

        print(
            f"Final move path: {move.path}"
        )

        print(
            f"Final captured squares: "
            f"{move.captured_squares}"
        )

        # Remove moving piece from origin.

        self.pieces.position[
            move.from_square
        ] = None

        # Remove captured pieces.

        for square in move.captured_squares:

            print(
                f"Removing piece from square "
                f"{square}"
            )

            self.pieces.position[
                square
            ] = None

        # Place moving piece at final destination.

        self.pieces.position[
            move.to_square
        ] = piece

        # Check promotion.

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