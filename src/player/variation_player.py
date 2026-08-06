import time

from src.renderer.timeline import Timeline


class VariationPlayer:
    """
    Plays a checkers variation move by move.
    Controls replay timing.
    """

    def __init__(self, game_state, renderer):

        self.game_state = game_state
        self.renderer = renderer
        self.timeline = Timeline()


    def play(self, variation):

        print(f"Playing: {variation.name}")
        print()


        # Starting position
        self.renderer.render_position(
            self.game_state
        )


        total_moves = len(
            variation.moves
        )


        # Initial board recognition hold
        print("Initial position hold...")
        time.sleep(3)



        for index, move in enumerate(
            variation.moves,
            start=1
        ):


            # HOLD BEFORE MOVE
            hold_time = self.timeline.hold_time(
                index,
                total_moves
            )

            print(
                f"Position hold: {hold_time}s"
            )

            time.sleep(
                hold_time
            )


            print(
                f"Applying move {index}/{total_moves}: {move}"
            )


            # Animate move
            self.renderer.animate(
                self.game_state,
                move
            )


            # Apply move
            self.game_state.apply_move(
                move
            )


            # Show result position
            self.renderer.render_position(
                self.game_state
            )


            # HOLD AFTER MOVE
            duration = self.timeline.wait_time(
                index,
                total_moves
            )

            print(
                f"Move duration: {duration}s"
            )

            time.sleep(
                duration
            )


        print("Variation complete.")
        print("Creating video...")


        self.renderer.video_output.create_video(
            self.renderer.image_output.saved_frames
        )