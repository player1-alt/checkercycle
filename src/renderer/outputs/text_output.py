from src.renderer.board_renderer import BoardRenderer


class TextOutput:
    """
    Displays the current game state as a board.
    """

    def __init__(self):
        self.board_renderer = BoardRenderer()


    def display(self, game_state):

        print("BOARD")
        print("-----")

        self.board_renderer.render(
            None,
            game_state.pieces
        )