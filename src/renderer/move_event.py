from src.renderer.move_event import MoveEvent
from src.renderer.timeline import Timeline

import time


class VariationPlayer:
    """
    Plays a checkers variation move by move.
    Creates MoveEvents for all outputs.
    """

    def __init__(self, game_state, renderer):

        self.game_state = game_state
        self.renderer = renderer
        self.timeline = Timeline()



    def play(self, variation):

        print(f"Playing: {variation.name}")
        print()


        self.renderer.render_position(
            self.game_state
        )


        total_moves = len(
            variation.moves
        )


        print("Initial position hold...")
        time.sleep(3)



        for index, move in enumerate(
            variation.moves,
            start=1
        ):


            hold = self.timeline.hold_time(
                index,
                total_moves
            )


            print(
                f"Position hold: {hold}s"
            )

            time.sleep(hold)



            start_square = move.path[0]

            end_square = move.path[-1]


            duration = self.timeline.wait_time(
                index,
                total_moves
            )


            event = MoveEvent(
                move,
                start_square,
                end_square,
                move.captured_squares,
                duration
            )


            event.describe()


            # VIDEO + ANIMATION
            self.renderer.animate(
                self.game_state,
                move
            )


            # GAME STATE UPDATE
            self.game_state.apply_move(
                move
            )


            # NEW BOARD
            self.renderer.render_position(
                self.game_state
            )


            time.sleep(duration)



        print("Variation complete.")

        self.renderer.video_output.create_video(
            self.renderer.image_output.saved_frames
        )