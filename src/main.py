from src.domains.checkers.book_loader import BookLoader
from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.game_state import GameState
from src.player.variation_player import VariationPlayer
from src.renderer.renderer import Renderer


def main():

    print("CheckerCycle Renderer")
    print("---------------------")
    print()

    loader = BookLoader()

    text = loader.load(
        "data/sample_game.txt"
    )

    parser = CheckersBookParser()

    variation = parser.parse_book(
        text,
        "Sample Game"
    )

    game_state = GameState()

    renderer = Renderer()

    player = VariationPlayer(
        game_state,
        renderer
    )

    player.play(variation)


if __name__ == "__main__":
    main()