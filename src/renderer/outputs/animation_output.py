from src.domains.checkers.square_mapper import SquareMapper


class AnimationOutput:
    """
    Converts renderer information into animation instructions.
    """

    def __init__(self, image_output=None):

        self.square_mapper = SquareMapper()
        self.image_output = image_output


    def generate_frames(self, start, end, steps=5):

        start_row, start_col = start
        end_row, end_col = end

        frames = []

        for i in range(steps + 1):

            progress = i / steps

            row = start_row + (end_row - start_row) * progress
            col = start_col + (end_col - start_col) * progress

            frames.append(
                (
                    round(row, 2),
                    round(col, 2)
                )
            )

        return frames


    def display(self, move):

        print("ANIMATION OUTPUT:")
        print("Animating piece:")
        print()

        print(f"Path: {move.path}")

        print()
        print("Animation frames:")


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


                # NEW:
                # save animation image
                if self.image_output:

                    self.image_output.save_animation_frame(
                        frame
                    )


            print()