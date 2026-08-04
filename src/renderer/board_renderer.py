class BoardRenderer:

    def render(self, board, pieces):

        for row in board.squares:
            print(" ".join(row))

        print()
        print("Pieces")
        print("------")

        for square in range(1, 33):
            print(f"{square:2}: {pieces.piece_at(square)}")