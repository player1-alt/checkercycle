class TextOutput:

    def display(self, game_state):

        print("Pieces")
        print("------")

        for square, piece in game_state.pieces.position.items():

            if piece is not None:
                print(f"{square:2}: {piece}")