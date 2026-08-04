from src.renderer.outputs.text_output import TextOutput
from src.renderer.outputs.animation_output import AnimationOutput
from src.renderer.outputs.audio_output import AudioOutput


class Renderer:
    """
    Controls all rendering outputs.
    """

    def __init__(self):

        self.text_output = TextOutput()
        self.animation_output = AnimationOutput()
        self.audio_output = AudioOutput()


    def render(self, game_state, move):

        if game_state is None:
            print("Cannot render invalid game state.")
            return

        print("====================================")
        print("THE RENDERER")
        print("Current game state:")
        print()

        # Current board/pieces
        self.text_output.display(game_state)

        print()

        # The move that happened
        self.animation_output.display(move)

        print()

        # Future: music mapping / MP3 generation
        self.audio_output.display(move)