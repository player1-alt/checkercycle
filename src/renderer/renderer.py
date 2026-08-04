from src.renderer.outputs.text_output import TextOutput


class Renderer:
    """
    Generic rendering engine.
    """

    def __init__(self):
        self.text_output = TextOutput()

    def render(self, input_data):
        print("====================================")
        print("THE RENDERER")
        print("Input received:")
        print(input_data)
        print()

        self.text_output.display(input_data)