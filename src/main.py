import sys

from src.domains.checkers.game_state import GameState
from src.domains.checkers.book_loader import BookLoader
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

    print("Starting position loaded")
    print()

    # ==========================
    # RENDERER
    # ==========================

    renderer = Renderer()

    # ==========================
    # LOAD GAME FROM TXT
    # ==========================

    book_loader = BookLoader()
    book_parser = CheckersBookParser()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "data/sample_game.txt"

    text = book_loader.load(filename)

    variation = book_parser.parse_book(
        text,
        "Imported Game"
    )

    # ==========================
    # PLAY GAME
    # ==========================

    player = VariationPlayer(
        game,
        renderer
    )

    player.play(
        variation
    )


if __name__ == "__main__":
    main()

