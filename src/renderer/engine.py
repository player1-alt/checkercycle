from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState

from src.renderer.board_renderer import BoardRenderer

from src.renderer.outputs.image_output import ImageOutput
from src.renderer.outputs.video_output import VideoOutput

from src.renderer.audio.audio_timeline import AudioTimeline


class RendererEngine:

    def __init__(self):

        print("Renderer Engine loaded")

        self.parser = CheckersBookParser()

        self.board_renderer = BoardRenderer()

        self.image_output = ImageOutput()

        self.video_output = VideoOutput()

        self.audio_timeline = AudioTimeline()

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

        # =====================================================
        # LOAD GAME FILE
        # =====================================================

        with open(
            game_file,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        # =====================================================
        # PARSE GAME
        # =====================================================

        print()
        print("Parsing moves...")

        variation = self.parser.parse_book(
            text
        )

        print(
            "Moves loaded:",
            len(variation.moves)
        )

        # =====================================================
        # CREATE STARTING POSITION
        # =====================================================

        print()
        print("Creating starting position...")

        game_state = GameState()

        self.image_output.reset()

        # =====================================================
        # START POSITION
        # =====================================================

        print()
        print("START POSITION")

        self.image_output.display(
            game_state
        )

        self.board_renderer.render(
            None,
            game_state.pieces
        )

        # =====================================================
        # PLAY EVERY MOVE
        #
        # Each resulting board position becomes a frame.
        #
        # Audio is built independently from the move sequence.
        # =====================================================

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

        frames = self.image_output.saved_frames

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
        # BUILD THREE SLIDESHOWS
        #
        # 13s
        # 8s
        # 4s
        # =====================================================

        print()
        print("=====================")
        print("BUILDING SLIDESHOWS")
        print("=====================")

        self.video_output.create_video(
            frames
        )

        # =====================================================
        # BUILD AUDIO
        # =====================================================

        print()
        print("=====================")
        print("BUILDING AUDIO")
        print("=====================")

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # Audio is based on the actual move paths.
        #
        # Example:
        #
        # 11-15
        # 23-19
        # 8-11
        # 22-17
        #
        # becomes:
        #
        # [11, 15, 23, 19, 8, 11, 22, 17]
        #
        # The AudioTimeline handles the three modes:
        #
        # 13s
        # 8s
        # 4s
        # -----------------------------------------------------

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

        if not audio_outputs:

            print(
                "No audio outputs created."
            )

        # -----------------------------------------------------
        # AUDIO OUTPUT IS A LIST
        # -----------------------------------------------------

        elif isinstance(
            audio_outputs,
            list
        ):

            for output in audio_outputs:

                print(
                    output
                )

        # -----------------------------------------------------
        # AUDIO OUTPUT IS A DICTIONARY
        #
        # This keeps the engine compatible if we later change
        # AudioTimeline to return:
        #
        # {
        #     13: "...mp3",
        #     8: "...mp3",
        #     4: "...mp3"
        # }
        # -----------------------------------------------------

        elif isinstance(
            audio_outputs,
            dict
        ):

            for mode, output in audio_outputs.items():

                print(
                    f"{mode}s:",
                    output
                )

        # -----------------------------------------------------
        # ANY OTHER RETURN TYPE
        # -----------------------------------------------------

        else:

            print(
                audio_outputs
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
            "audio": audio_outputs
        }