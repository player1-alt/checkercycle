class AnimationOutput:
    """
    Converts renderer information into animation instructions.
    """

    def display(self, data):
        print("ANIMATION OUTPUT:")
        print(f"Animating piece:")
        print(f"Square {data.from_square} -> Square {data.to_square}")