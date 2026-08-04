from src.domains.checkers.game_state import GameState
from src.domains.checkers.book_parser import CheckersBookParser
from src.player.variation_player import VariationPlayer
from src.renderer.renderer import Renderer


def main():

    # Create game state
    game_state = GameState()

    # Load game from file
    with open("data/sample_game.txt", "r") as file:
        notation = file.read()

    parser = CheckersBookParser()

    variation = parser.parse_book(
        notation,
        "Sample Game"
    )

    # Create renderer and player
    renderer = Renderer()

    player = VariationPlayer(
        game_state,
        renderer
    )

    # Play imported game
    player.play(variation)


if __name__ == "__main__":
    main()