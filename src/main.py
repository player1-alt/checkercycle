from src.renderer.pieces import Pieces


def main():

    pieces = Pieces()

    for square in range(1, 33):
        print(square, ":", pieces.piece_at(square))


if __name__ == "__main__":
    main()