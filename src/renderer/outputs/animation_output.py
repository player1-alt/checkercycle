from src.domains.checkers.square_mapper import SquareMapper


class AnimationOutput:
    """
    Converts renderer information into animation instructions.
    """

    def __init__(self):
        self.square_mapper = SquareMapper()


    def generate_frames(self, start, end, steps=5):
        """
        Creates movement frames between two coordinates.
        """

        start_row, start_col = start
        end_row, end_col = end

        frames = []

        for i in range(steps + 1):

            progress = i / steps

            row = start_row + (end_row - start_row) * progress
            col = start_col + (end_col - start_col) * progress

            frames.append(
                (round(row, 2), round(col, 2))
            )

        return frames


    def display(self, move):

        print("ANIMATION OUTPUT:")
        print("Animating piece:")
        print()

        print(f"Path: {move.path}")

        print()
        print("Animation frames:")

        # Animate each part of the path
        for index in range(len(move.path) - 1):

            start_square = move.path[index]
            end_square = move.path[index + 1]

            start = self.square_mapper.coordinates(
                start_square
            )

            end = self.square_mapper.coordinates(
                end_square
            )

            print(
                f"Jump {start_square} -> {end_square}"
            )

            print(
                f"Coordinates {start} -> {end}"
            )

            frames = self.generate_frames(
                start,
                end
            )

            for number, frame in enumerate(
                frames,
                start=1
            ):
                print(
                    f"Frame {number}: {frame}"
                )

            print()


        # Capture events
        if move.captured_squares:

            print("CAPTURE EVENTS:")
            print()

            for square in move.captured_squares:

                print(
                    f"Remove piece from square {square}"
                )

            print()