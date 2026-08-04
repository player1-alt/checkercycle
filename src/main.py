from src.renderer.renderer import Renderer
from src.domains.checkers.book_parser import CheckersBookParser


def main():
    renderer = Renderer()

    book_parser = CheckersBookParser()

    book = """
    11-15
    15-18
    22-17
    """

    moves = book_parser.parse_book(book)

    for move in moves:
        renderer.render(move)


if __name__ == "__main__":
    main()

