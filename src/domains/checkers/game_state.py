from src.renderer.pieces import Pieces
from src.domains.checkers.square_mapper import SquareMapper


class GameState:

    def __init__(self):

        self.pieces = Pieces()
        self.square_mapper = SquareMapper()


    # ==========================
    # FIND MULTI JUMP PATH
    # ==========================

    def find_jump_path(
        self,
        from_square,
        to_square,
        moving_piece
    ):

        target = self.square_mapper.coordinates(
            to_square
        )

        board = dict(
            self.pieces.position
        )

        board[from_square] = None

        return self._search_jump_path(
            from_square,
            target,
            moving_piece,
            board,
            [from_square],
            []
        )



    def _search_jump_path(
        self,
        current_square,
        target_coordinates,
        moving_piece,
        board,
        path,
        captured
    ):


        current_row, current_col = (
            self.square_mapper.coordinates(
                current_square
            )
        )


        target_row, target_col = target_coordinates


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
            (-1,-1),
            (-1,1),
            (1,-1),
            (1,1)
        ]


        for dr,dc in directions:


            middle_row = current_row + dr
            middle_col = current_col + dc

            land_row = current_row + dr*2
            land_col = current_col + dc*2


            if not self._valid_coordinates(
                land_row,
                land_col
            ):
                continue


            try:

                middle_square = self.square_mapper.square(
                    middle_row,
                    middle_col
                )

                landing_square = self.square_mapper.square(
                    land_row,
                    land_col
                )

            except KeyError:

                continue


            middle_piece = board.get(
                middle_square
            )

            landing_piece = board.get(
                landing_square
            )


            if middle_piece is None:
                continue


            if middle_piece.color == moving_piece.color:
                continue


            if landing_piece is not None:
                continue


            if middle_square in captured:
                continue



            board[current_square] = None
            board[middle_square] = None
            board[landing_square] = moving_piece


            path.append(
                landing_square
            )

            captured.append(
                middle_square
            )


            result = self._search_jump_path(
                landing_square,
                target_coordinates,
                moving_piece,
                board,
                path,
                captured
            )


            if result:
                return result



            board[landing_square] = None
            board[middle_square] = middle_piece
            board[current_square] = moving_piece


            path.pop()
            captured.pop()



        return None



    def _valid_coordinates(
        self,
        row,
        col
    ):

        return (
            0 <= row < 8
            and 0 <= col < 8
        )
    # ==========================
    # APPLY MOVE
    # ==========================

    def apply_move(
        self,
        move
    ):

        moving_piece = self.pieces.piece_at(
            move.from_square
        )


        # SAFETY CHECK
        # Prevent None.color crash

        if moving_piece is None:

            print(
                "ERROR: No piece found on square",
                move.from_square
            )

            print(
                "Move ignored:",
                move.path
            )

            return



        # ==========================
        # AUTO MULTI-JUMP DETECTION
        # ==========================

        if (
            not move.is_capture
            and not move.captured_squares
            and len(move.path) == 2
        ):


            result = self.find_jump_path(
                move.from_square,
                move.to_square,
                moving_piece
            )


            if result is not None:

                discovered_path, discovered_capture = result


                move.path = discovered_path

                move.captured_squares = (
                    discovered_capture
                )

                move.is_capture = True


                print()
                print(
                    "AUTOMATIC MULTI-JUMP DETECTED"
                )

                print(
                    "Path:",
                    move.path
                )

                print(
                    "Captured:",
                    move.captured_squares
                )

                print()



        print(
            "Final move path:",
            move.path
        )


        print(
            "Final captured squares:",
            move.captured_squares
        )



        # Remove from starting square

        self.pieces.position[
            move.from_square
        ] = None



        # Remove captures

        for square in move.captured_squares:


            print(
                "Removing piece from square",
                square
            )


            self.pieces.position[
                square
            ] = None




        # Final destination

        final_square = move.path[-1]



        self.pieces.position[
            final_square
        ] = moving_piece



        # Promotion

        self.check_promotion(
            moving_piece,
            final_square
        )




    # ==========================
    # PROMOTION
    # ==========================


    def check_promotion(
        self,
        piece,
        square
    ):


        if piece is None:

            return



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