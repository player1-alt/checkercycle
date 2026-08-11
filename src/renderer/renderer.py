from src.renderer.outputs.text_output import TextOutput
from src.renderer.outputs.animation_output import AnimationOutput
from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput


class Renderer:
    """
    Controls all rendering outputs.

    Receives MoveEvents and sends them to:
    - Animation
    - Video
    """

    def __init__(self):

        self.image_output = ImageOutput()

        self.text_output = TextOutput()

        self.animation_output = AnimationOutput(
            self.image_output
        )

        self.video_output = VideoOutput()

    def render_position(
        self,
        game_state
    ):

        if game_state is None:
            return

        print("====================================")
        print("BOARD POSITION")
        print()

        self.text_output.display(
            game_state
        )

        print()

        self.image_output.display(
            game_state
        )

        print()

    def animate(
        self,
        game_state,
        event
    ):

        if game_state is None:
            return

        print("ANIMATION")
        print()

        self.animation_output.display(
            game_state,
            event
        )

        print()