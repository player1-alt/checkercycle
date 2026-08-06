from src.domains.checkers.game_state import GameState
from src.domains.checkers.book_parser import CheckersBookParser

from src.player.variation_player import VariationPlayer
from src.renderer.renderer import Renderer



def main():

    print("CheckerCycle Renderer")
    print("---------------------")
    print()



    # ==========================
    # NORMAL GAME START
    # ==========================

    print("STARTING POSITION TEST")
    print("---------------------")


    game = GameState()


    print(
        "Starting position loaded"
    )


    print()



    # ==========================
    # RENDERER
    # ==========================

    renderer = Renderer()



    # ==========================
    # BOOK PARSER TEST
    # ==========================

    book_parser = CheckersBookParser()



    variation = book_parser.parse_book(
        """
        9-13
        22-18
        13-17
        """,
        "Opening Test"
    )



    player = VariationPlayer(
        game,
        renderer
    )


    player.play(
        variation
    )



if __name__ == "__main__":

    main()