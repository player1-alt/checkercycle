from src.renderer.outputs.text_output import TextOutput
from src.renderer.outputs.animation_output import AnimationOutput
from src.renderer.outputs.audio_output import AudioOutput
from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput



class Renderer:
    """
    Controls all rendering outputs.
    """


    def __init__(self):

        # Static board image output
        self.image_output = ImageOutput()


        # Text board display
        self.text_output = TextOutput()


        # Animation frame generator
        self.animation_output = AnimationOutput(
            self.image_output
        )


        # Audio system
        self.audio_output = AudioOutput()


        # Video exporter
        self.video_output = VideoOutput()



    def render(self, game_state, move):

        if game_state is None:

            print(
                "Cannot render invalid game state."
            )

            return



        print(
            "===================================="
        )

        print(
            "THE RENDERER"
        )

        print(
            "Current game state:"
        )

        print()



        # Display text board
        self.text_output.display(
            game_state
        )


        print()



        # Save current board frame
        self.image_output.display(
            game_state
        )


        print()



        # Generate moving piece animation frames
        self.animation_output.display(
            game_state,
            move
        )


        print()



        # Prepare audio mapping
        self.audio_output.display(
            move
        )