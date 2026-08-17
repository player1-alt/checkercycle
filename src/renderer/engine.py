from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState

from src.renderer.board_renderer import BoardRenderer

from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput

from src.renderer.audio.audio_timeline import AudioTimeline

from src.renderer.naming.naming_node import NamingNode


class RendererEngine:

    def __init__(self):

        print("Renderer Engine loaded")

        self.parser = CheckersBookParser()

        self.board_renderer = BoardRenderer()

        self.image_output = ImageOutput()

        self.video_output = VideoOutput()

        self.audio_timeline = AudioTimeline()

        self.naming_node = NamingNode()

    # =========================================================
    # RENDER
    # =========================================================

    def render(self, game_file):

        print()
        print("---------------------")
        print("CHECKERCYCLE RENDER")
        print("---------------------")

        print()
        print("Loading game:")
        print(game_file)

        # -----------------------------------------------------
        # LOAD GAME FILE
        # -----------------------------------------------------

        with open(
            game_file,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        # -----------------------------------------------------
        # PARSE GAME
        # -----------------------------------------------------

        print()
        print("Parsing moves...")

        variation = self.parser.parse_book(
            text
        )

        print(
            "Moves loaded:",
            len(variation.moves)
        )

        # -----------------------------------------------------
        # CREATE STARTING POSITION
        # -----------------------------------------------------

        print()
        print("Creating starting position...")

        game_state = GameState()

        self.image_output.reset()

        # -----------------------------------------------------
        # START POSITION
        # -----------------------------------------------------

        print()
        print("START POSITION")

        self.image_output.display(
            game_state
        )

        self.board_renderer.render(
            None,
            game_state.pieces
        )

        # -----------------------------------------------------
        # PLAY EVERY MOVE
        # -----------------------------------------------------

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

        # =====================================================
        # COLLECT SLIDESHOW FRAMES
        # =====================================================

        print()
        print("=====================")
        print("SLIDESHOW FRAMES")
        print("=====================")

        frames = (
            self.image_output.saved_frames
        )

        for frame in frames:

            print(
                frame
            )

        print()
        print(
            "FRAMES CREATED:",
            len(frames)
        )

        print("=====================")

        # =====================================================
        # BUILD THREE SILENT SLIDESHOWS
        # =====================================================

        print()
        print("=====================")
        print("BUILDING SLIDESHOWS")
        print("=====================")

        self.video_output.create_video(
            frames
        )

        # =====================================================
        # BUILD THREE AUDIO FILES
        # =====================================================

        print()
        print("=====================")
        print("BUILDING AUDIO")
        print("=====================")

        audio_outputs = (
            self.audio_timeline.build(
                variation.moves
            )
        )

        # =====================================================
        # REPORT AUDIO OUTPUTS
        # =====================================================

        print()
        print("=====================")
        print("AUDIO OUTPUTS")
        print("=====================")

        if audio_outputs:

            for output in audio_outputs:

                print(
                    output
                )

        else:

            print(
                "No audio outputs created."
            )

        # =====================================================
        # NAMING NODE
        #
        # IMPORTANT:
        #
        # The original TXT file is NOT renamed,
        # moved, copied, or deleted.
        #
        # NamingNode only renames the generated
        # CheckerCycle audio/video files.
        # =====================================================

        print()
        print("=====================")
        print("RUNNING NAMING NODE")
        print("=====================")

        named_outputs = (
            self.naming_node.rename_outputs(
                game_file
            )
        )

        # =====================================================
        # FINAL OUTPUT REPORT
        # =====================================================

        print()
        print("=====================")
        print("FINAL OUTPUTS")
        print("=====================")

        for output in named_outputs:

            print(
                output
            )

        # =====================================================
        # COMPLETE
        # =====================================================

        print()
        print("=====================")
        print("RENDER COMPLETE")
        print("=====================")
        print()

        return {
            "frames": frames,
            "audio": audio_outputs,
            "named_outputs": named_outputs
        }