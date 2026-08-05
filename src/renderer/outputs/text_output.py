from src.renderer.board_renderer import BoardRenderer
from src.renderer.outputs.image_output import ImageOutput


class TextOutput:
    """
    Displays the current game state as a board and saves a PNG frame.
    """

    def __init__(self):
        self.board_renderer = BoardRenderer()
        self.image_output = ImageOutput()
        self.frame_counter = 1


    def display(self, game_state):

        print("BOARD")
        print("-----")

        self.board_renderer.render(
            None,
            game_state.pieces
        )

        filename = f"frame{self.frame_counter:04d}.png"

        self.image_output.export(
            game_state.pieces,
            filename
        )

        self.frame_counter += 1