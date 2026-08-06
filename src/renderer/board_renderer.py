from src.domains.checkers.square_mapper import SquareMapper


class BoardRenderer:
    """
    Converts game state into a visual board display.
    """

    def __init__(self):
        self.square_mapper = SquareMapper()


    def render(self, board, pieces):

        display_board = []

        # Create empty 8x8 board
        for row in range(8):

            current_row = []

            for column in range(8):

                if (row + column) % 2 == 0:
                    current_row.append(".")
                else:
                    current_row.append(" ")

            display_board.append(current_row)


        # Place pieces on board
        for square, piece in pieces.position.items():

            if piece is not None:

                row, column = self.square_mapper.coordinates(square)

                display_board[row][column] = piece.symbol()


        # Print board
        print()

        for row in display_board:
            print(" ".join(f"{cell:>2}" for cell in row))

        print()