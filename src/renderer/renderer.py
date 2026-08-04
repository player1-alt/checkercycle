from src.renderer.outputs.text_output import TextOutput
from src.renderer.outputs.animation_output import AnimationOutput
from src.renderer.outputs.audio_output import AudioOutput


class Renderer:

    def __init__(self):
        self.text_output = TextOutput()
        self.animation_output = AnimationOutput()
        self.audio_output = AudioOutput()

    def render(self, input_data):

        if input_data is None:
            print("Cannot render invalid input.")
            return

        print("====================================")
        print("THE RENDERER")
        print("Input received:")
        print(input_data)
        print()

        self.text_output.display(input_data)
        print()

        self.animation_output.display(input_data)
        print()

        self.audio_output.display(input_data)