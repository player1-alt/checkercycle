from src.renderer.renderer import Renderer
from src.domains.checkers.move import Move


def main():
    renderer = Renderer()

    move = Move(11, 15)

    renderer.render(move)


if __name__ == "__main__":
    main()


