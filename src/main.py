from src.domains.checkers.game_state import GameState
from src.domains.checkers.game_state_loader import GameStateLoader
from src.domains.checkers.move import Move

from src.renderer.renderer import Renderer


def main():

    game_state = GameState()

    loader = GameStateLoader()


    # Load a single white piece
    loader.load(
        game_state,
        {
            5: "white"
        },
        clear=True
    )


    print("BEFORE MOVE")
    print(game_state.pieces.position)


    # White moves to the king row
    move = Move(
        [5, 1]
    )


    game_state.apply_move(move)


    print()
    print("AFTER MOVE")
    print(game_state.pieces.position)


    print()
    print("KING STATUS:")
    piece = game_state.pieces.position[1]

    print(piece.king)
    print(piece.symbol())


    renderer = Renderer()

    renderer.render(
        game_state,
        move
    )


if __name__ == "__main__":
    main()