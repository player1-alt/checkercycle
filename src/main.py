from src.renderer.renderer import Renderer
from src.domains.checkers.parser import CheckersParser


def main():
    renderer = Renderer()

    parser = CheckersParser()

    move = parser.parse("11-15")

    renderer.render(move)


if __name__ == "__main__":
    main()


