from src.renderer.renderer import Renderer
from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.variation import Variation
from src.player.variation_player import VariationPlayer


def main():
    # Create the renderer
    renderer = Renderer()

    # Create the book parser
    book_parser = CheckersBookParser()

    # Sample checkers variation
    book = """
11-15
23-19
8-11
22-17
"""

    # Parse the moves
    moves = book_parser.parse_book(book)

    # Create a variation
    variation = Variation(
        "Test Variation",
        moves
    )

    # Display variation information
    print(variation.describe())
    print()

    # Create the player with a 2-second interval
    player = VariationPlayer(renderer, interval=2)

    # Play the variation
    player.play(variation)


if __name__ == "__main__":
    main()