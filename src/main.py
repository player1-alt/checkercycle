from src.renderer.board import Board
from src.renderer.board_renderer import BoardRenderer
from src.renderer.pieces import Pieces


def main():

    board = Board()

    pieces = Pieces()

    renderer = BoardRenderer()

    renderer.render(board, pieces)


if __name__ == "__main__":
    main()