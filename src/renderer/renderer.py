from src.renderer.outputs.text_output import TextOutput
from src.renderer.outputs.animation_output import AnimationOutput
from src.renderer.outputs.audio_output import AudioOutput
from src.renderer.outputs.image_output import ImageOutput


class Renderer:
    """
    Controls all rendering outputs.
    """

    def __init__(self):

        self.text_output = TextOutput()

        self.image_output = ImageOutput()

        self.animation_output = AnimationOutput(
            self.image_output
        )

        self.audio_output = AudioOutput()


    def render(self, game_state, move):

        if game_state is None:

            print(
                "Cannot render invalid game state."
            )

            return


        print("====================================")
        print("THE RENDERER")
        print("Current game state:")
        print()


        # Text board output
        self.text_output.display(
            game_state
        )


        print()


        # Save current board image
        self.image_output.display(
            game_state
        )


        print()


        # Generate animation frames
        self.animation_output.display(
            move
        )


        print()


        # Audio placeholder
        self.audio_output.display(
            move
        )