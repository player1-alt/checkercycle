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


        total_moves = len(variation.moves)



        for index, move in enumerate(
            variation.moves,
            start=1
        ):


            print(
                f"Applying move {index}/{total_moves}: {move}"
            )


            # Update board position
            self.game_state.apply_move(
                move
            )


            # Render board + animation frames
            self.renderer.render(
                self.game_state,
                move
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



        # GAME FINISHED
        print("Variation complete.")
        print("Creating video...")


        self.renderer.video_output.create_video()