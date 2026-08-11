from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState

from src.renderer.board_renderer import BoardRenderer

from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput

from src.renderer.timeline import Timeline


class RendererEngine:

    def __init__(self):

        print("Renderer Engine loaded")

        self.parser = CheckersBookParser()

        self.board_renderer = BoardRenderer()

        self.image_output = ImageOutput()

        self.video_output = VideoOutput()

        self.timeline = Timeline()

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

        variation = self.parser.parse_book(
            text
        )

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

        # ---------------------------------------------
        # PLAY EVERY MOVE AND SAVE RESULTING POSITIONS
        # ---------------------------------------------

        for move in variation.moves:

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

        # ---------------------------------------------
        # FRAME TIMELINE
        # ---------------------------------------------

        print()
        print("=====================")
        print("FRAME TIMELINE")
        print("=====================")

        frames = (
            self.image_output.saved_frames
        )

        frame_duration = 13.0

        for frame in frames:

            print(
                frame,
                "->",
                frame_duration,
                "seconds"
            )

        print()
        print("=====================")

        print(
            "FRAMES CREATED:",
            len(frames)
        )

        print("=====================")

        # ---------------------------------------------
        # BUILD SILENT MP4
        # ---------------------------------------------

        print()
        print("Building MP4...")

        self.video_output.create_video(
            frames
        )

        print()
        print("=====================")
        print("RENDER COMPLETE")
        print("=====================")