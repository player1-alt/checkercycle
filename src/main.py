
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
    # CHECK INPUT FILE
    # ==========================

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("No game file supplied.")
        print()
        print("Usage:")
        print("    CheckerCycle.exe <game.txt>")
        print()
        return

    # ==========================
    # LOAD GAME
    # ==========================

    book_loader = BookLoader()
    book_parser = CheckersBookParser()

    try:
        text = book_loader.load(filename)

    except FileNotFoundError:
        print(f"Game file not found: {filename}")
        print()
        return

    except OSError as error:
        print(f"Could not open game file: {error}")
        print()
        return

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
    # PARSE GAME
    # ==========================

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

