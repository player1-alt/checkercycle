
from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState

from src.renderer.board_renderer import BoardRenderer

from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput

from src.renderer.timeline import Timeline

from src.renderer.final_output import FinalOutput

from src.renderer.audio.audio_timeline import AudioTimeline


class RendererEngine:

    def __init__(self):

        print("Renderer Engine loaded")

        self.parser = CheckersBookParser()

        self.board_renderer = BoardRenderer()

        self.image_output = ImageOutput()

        self.video_output = VideoOutput()

        self.timeline = Timeline()

        self.audio_timeline = AudioTimeline()

        self.final_output = FinalOutput()


    def render(self, game_file):

        print()
        print("---------------------")
        print("CHECKERCYCLE RENDER")
        print("---------------------")

        print()
        print("Loading game:")
        print(game_file)

        with open(
            game_file,
            "r"
        ) as file:

            text = file.read()

        print()
        print("Parsing moves...")

        variation = self.parser.parse_book(text)

        print(
            "Moves loaded:",
            len(variation.moves)
        )

        print()
        print("Creating starting position...")

        game_state = GameState()

        self.image_output.reset()

        print()
        print("START POSITION")

        self.image_output.display(
            game_state
        )

        self.board_renderer.render(
            None,
            game_state.pieces
        )

        move_paths = []

        for move in variation.moves:

            move_paths.append(
                move
            )

            game_state.apply_move(
                move
            )

            self.image_output.display(
                game_state
            )

            self.board_renderer.render(
                None,
                game_state.pieces
            )

        print()
        print("=====================")
        print("FRAME TIMELINE")
        print("=====================")

        frames = self.image_output.saved_frames

        timeline_data = []

        frame_duration = self.timeline.square_duration()

        for index, frame in enumerate(frames):

            duration = frame_duration

            print(
                frame,
                "->",
                duration,
                "seconds"
            )

            timeline_data.append(
                {
                    "frame": frame,
                    "duration": duration
                }
            )

        print()
        print("=====================")
        print(
            "FRAMES CREATED:",
            len(frames)
        )
        print("=====================")

        print()
        print("Building MP4...")

        self.video_output.create_video(
            frames,
            timeline_data
        )

        print()
        print("Building audio timeline...")

        audio_events = []

        # --------------------------------------------------
        # FRAME 0 = starting position
        #
        # The starting square is the first square of the
        # first move.
        # --------------------------------------------------

        if move_paths:

            first_move = move_paths[0]

            if hasattr(first_move, "path"):

                start_path = first_move.path

                if start_path:

                    audio_events.append(
                        {
                            "path": [
                                start_path[0]
                            ],
                            "duration": frame_duration
                        }
                    )

                else:

                    audio_events.append(
                        {
                            "path": [],
                            "duration": frame_duration
                        }
                    )

        else:

            audio_events.append(
                {
                    "path": [],
                    "duration": frame_duration
                }
            )

        # --------------------------------------------------
        # Remaining frames
        #
        # Each frame represents the position AFTER the
        # previous move, so its audio is the destination
        # square of that move.
        # --------------------------------------------------

        for move in move_paths:

            if hasattr(move, "path"):

                path = move.path

                if path:

                    destination = path[-1]

                    audio_events.append(
                        {
                            "path": [
                                destination
                            ],
                            "duration": frame_duration
                        }
                    )

                else:

                    audio_events.append(
                        {
                            "path": [],
                            "duration": frame_duration
                        }
                    )

        # Make sure audio events exactly match frames.

        audio_events = audio_events[:len(frames)]

        while len(audio_events) < len(frames):

            audio_events.append(
                {
                    "path": [],
                    "duration": frame_duration
                }
            )

        self.audio_timeline.build(
            audio_events
        )

        print()
        print("Building final video...")

        self.final_output.combine()

        print()
        print("RENDER COMPLETE")
