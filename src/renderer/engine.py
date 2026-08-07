from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState
from src.renderer.board_renderer import BoardRenderer


class RendererEngine:


    def __init__(self):

        print("Renderer Engine loaded")

        self.parser = CheckersBookParser()

        self.board_renderer = BoardRenderer()



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


        print()
        print("START POSITION")
        print("----------------")


        self.board_renderer.render(
            None,
            game_state.pieces
        )



        move_number = 1


        for move in variation.moves:


            print()
            print("================")
            print(
                "MOVE",
                move_number
            )

            print("================")


            game_state.apply_move(
                move
            )


            self.board_renderer.render(
                None,
                game_state.pieces
            )


            move_number += 1



        print()
        print("=====================")
        print("RENDER COMPLETE")
        print("=====================")