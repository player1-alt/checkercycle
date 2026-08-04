from src.renderer.renderer import Renderer
from src.domains.checkers.book_loader import BookLoader
from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.variation import Variation
from src.player.variation_player import VariationPlayer


def main():
    renderer = Renderer()

    loader = BookLoader()

    book_parser = CheckersBookParser()

    # Load the game from a text file
    book = loader.load("data/sample_game.txt")

    moves = book_parser.parse_book(book)

    variation = Variation(
        "Sample Game",
        moves
    )

    print(variation.describe())
    print()

    player = VariationPlayer(renderer, interval=2)

    player.play(variation)


if __name__ == "__main__":
    main()