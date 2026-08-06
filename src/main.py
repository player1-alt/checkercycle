from src.domains.checkers.game_state import GameState
from src.domains.checkers.variation import Variation
from src.domains.checkers.parser import CheckersParser

from src.player.variation_player import VariationPlayer
from src.renderer.renderer import Renderer


def main():

    print("CheckerCycle Renderer")
    print("---------------------")
    print()


    # ==========================
    # KING TEST
    # ==========================

    print("KING TEST")
    print("---------------------")

    king_state = GameState()

    piece = king_state.pieces.piece_at(29)

    print(
        "Piece at square 29:",
        piece.symbol()
    )

    print()



    # ==========================
    # PROMOTION TEST
    # ==========================

    print("PROMOTION TEST")
    print("---------------------")

    test_state = GameState()

    piece = test_state.pieces.piece_at(25)

    test_state.pieces.position[25] = None

    test_state.pieces.position[29] = piece


    test_state.check_promotion(
        piece,
        29
    )


    print(
        "Piece at square 29:",
        test_state.pieces.piece_at(29).symbol()
    )

    print()



    # ==========================
    # SAMPLE GAME
    # ==========================

    game_state = GameState()

    renderer = Renderer()


    parser = CheckersParser()


    moves_text = """
    11-15
    23-19
    8-11
    22-18
    15-22
    25-18
    """


    moves = []


    for line in moves_text.strip().splitlines():

        move = parser.parse(line)

        if move:
            moves.append(move)



    variation = Variation(
        "Sample Game",
        moves
    )


    player = VariationPlayer(
        game_state,
        renderer
    )


    player.play(
        variation
    )



if __name__ == "__main__":

    main()