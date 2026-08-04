from src.domains.checkers.square_mapper import SquareMapper


class AnimationOutput:
    """
    Converts renderer information into animation instructions.
    """

    def __init__(self):
        self.square_mapper = SquareMapper()


    def display(self, move):

        print("ANIMATION OUTPUT:")
        print("Animating piece:")

        start = self.square_mapper.coordinates(move.from_square)
        end = self.square_mapper.coordinates(move.to_square)

        print(f"Square {move.from_square} -> Square {move.to_square}")

        print(
            f"Coordinates {start} -> {end}"
        )

        print(
            "Animation path generated."
        )