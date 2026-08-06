import time

from src.renderer.timeline import Timeline


class VariationPlayer:
    """
    Plays a checkers variation move by move.
    Updates the game state and controls replay timing.
    """

    def __init__(self, game_state, renderer):

        self.game_state = game_state
        self.renderer = renderer
        self.timeline = Timeline()

    def play(self, variation):

        print(f"Playing: {variation.name}")
        print()

        # Show starting position
        self.renderer.render_position(
            self.game_state
        )

        total_moves = len(
            variation.moves
        )

        for index, move in enumerate(
            variation.moves,
            start=1
        ):

            print(
                f"Applying move {index}/{total_moves}: {move}"
            )

            # Animate from the current position
            self.renderer.animate(
                self.game_state,
                move
            )

            # Apply the move
            self.game_state.apply_move(
                move
            )

            # Show the new position
            self.renderer.render_position(
                self.game_state
            )

            duration = self.timeline.wait_time(
                index,
                total_moves
            )

            print(
                f"Move duration: {duration}s"
            )

            print()

            time.sleep(duration)

        print("Variation complete.")
        print("Creating video...")

        self.renderer.video_output.create_video(
            self.renderer.image_output.saved_frames
        )