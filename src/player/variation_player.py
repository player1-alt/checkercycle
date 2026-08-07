import time

from src.renderer.timeline import Timeline
from src.renderer.move_event import MoveEvent


class VariationPlayer:
    """
    Plays a checkers variation move by move.

    MoveEvent is the communication layer between:
    - Animation
    - Audio
    - Timing
    - Video
    """

    def __init__(self, game_state, renderer):

        self.game_state = game_state
        self.renderer = renderer
        self.timeline = Timeline()

        # Stores all MoveEvents for video timing
        self.events = []



    def play(self, variation):

        print(f"Playing: {variation.name}")
        print()


        # Starting board position

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

            print(
                "PLAYING MOVE:",
                index,
                move.path
            )


            # Time before move

            hold = self.timeline.hold_time(
                index,
                total_moves
            )


            print(
                f"Position hold: {hold}s"
            )


            time.sleep(hold)



            # Movement duration

            duration = self.timeline.wait_time(
                index,
                total_moves
            )


            # =========================================
            # SAVE PIECE BEFORE BOARD CHANGES
            # =========================================

            moving_piece = (
                self.game_state.pieces.piece_at(
                    move.path[0]
                )
            )


            # =========================================
            # CREATE MOVE EVENT
            # =========================================

            event = MoveEvent(

                move,

                move.path[0],

                move.path[-1],

                move.captured_squares,

                duration,

                hold,

                moving_piece

            )


            # Save event for video

            self.events.append(
                event
            )



            event.describe()

            print()



            # =========================================
            # ANIMATION + AUDIO
            # =========================================

            self.renderer.animate(
                self.game_state,
                event
            )



            # =========================================
            # APPLY MOVE AFTER ANIMATION
            # =========================================

            self.game_state.apply_move(
                move
            )



            # Render resulting position

            self.renderer.render_position(
                self.game_state
            )



            print(
                f"Move duration: {duration}s"
            )


            time.sleep(duration)



        print(
            "Variation complete."
        )

        print(
            "Creating video..."
        )



        # Send frames + timing events to video

        self.renderer.video_output.create_video(
            self.renderer.image_output.saved_frames,
            self.events
        )