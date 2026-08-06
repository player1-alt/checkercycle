import time

from src.renderer.timeline import Timeline
from src.renderer.move_event import MoveEvent
from src.renderer.settings import SETTINGS

class VariationPlayer:
    """
    Plays a checkers variation move by move.

    MoveEvent is the communication layer
    between:
    - Animation
    - Audio
    - Timing
    - Video
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


        print("Initial position hold...")

        time.sleep(
            SETTINGS["initial_hold"]
)




        for index, move in enumerate(
            variation.moves,
            start=1
        ):


            # Hold before move

            hold = self.timeline.hold_time(
                index,
                total_moves
            )

            print(
                f"Position hold: {hold}s"
            )

            time.sleep(hold)



            # Calculate duration

            duration = self.timeline.wait_time(
                index,
                total_moves
            )


            # Create event FIRST

            event = MoveEvent(

                move,

                move.path[0],

                move.path[-1],

                move.captured_squares,

                duration

            )


            event.describe()

            print()



            # Animate using event

            self.renderer.animate(
                self.game_state,
                event
            )



            # Apply actual game move

            self.game_state.apply_move(
                move
            )



            # Render new board

            self.renderer.render_position(
                self.game_state
            )


            print(
                f"Move duration: {duration}s"
            )

            time.sleep(duration)



        print("Variation complete.")

        print("Creating video...")


        self.renderer.video_output.create_video(
            self.renderer.image_output.saved_frames
        )