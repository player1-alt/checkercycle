from src.domains.checkers.square_mapper import SquareMapper


class AnimationOutput:
    """
    Creates animation frames for real checker pieces.

    Receives MoveEvent so animation and video
    share the same move data.
    """

    def __init__(self, image_output=None):

        self.square_mapper = SquareMapper()

        self.image_output = image_output

    def generate_frames(
        self,
        start,
        end,
        steps=5
    ):

        start_row, start_col = start
        end_row, end_col = end

        frames = []

        for i in range(steps + 1):

            progress = i / steps

            row = (
                start_row
                + (end_row - start_row)
                * progress
            )

            col = (
                start_col
                + (end_col - start_col)
                * progress
            )

            frames.append(
                (
                    round(row, 2),
                    round(col, 2)
                )
            )

        return frames

    def display(
        self,
        game_state,
        event
    ):

        print("ANIMATION OUTPUT:")
        print("Animating piece:")
        print()

        move = event.move

        print(
            f"Path: {move.path}"
        )

        print()

        # =====================================
        # GET PIECE FROM EVENT SNAPSHOT
        # =====================================

        moving_piece = event.moving_piece

        if moving_piece is None:

            print(
                "WARNING: No moving piece found"
            )

            return

        # =====================================
        # ANIMATE EACH SEGMENT OF THE MOVE
        # =====================================

        for index in range(
            len(move.path) - 1
        ):

            start_square = (
                move.path[index]
            )

            end_square = (
                move.path[index + 1]
            )

            start = (
                self.square_mapper.coordinates(
                    start_square
                )
            )

            end = (
                self.square_mapper.coordinates(
                    end_square
                )
            )

            print(
                f"Moving "
                f"{start_square} -> "
                f"{end_square}"
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

                if self.image_output:

                    self.image_output.save_animation_frame(
                        game_state,
                        moving_piece,
                        frame
                    )

            print()

        # =====================================
        # CAPTURE EVENTS
        # =====================================

        if event.captured_squares:

            print(
                "CAPTURE EVENTS:"
            )

            for square in event.captured_squares:

                print(
                    f"Remove piece from {square}"
                )