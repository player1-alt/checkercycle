from src.renderer.renderer import Renderer
from src.domains.checkers.book_parser import CheckersBookParser
from src.domains.checkers.variation import Variation


def main():
    renderer = Renderer()

    book_parser = CheckersBookParser()

    book = """
11-15
23-19
8-11
22-17
"""

    moves = book_parser.parse_book(book)

    variation = Variation(
        "Test Variation",
        moves
    )

    print(variation.describe())

    for move in variation.moves:
        renderer.render(move)


if __name__ == "__main__":
    main()