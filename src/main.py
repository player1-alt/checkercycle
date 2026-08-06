from src.domains.checkers.game_state import GameState
from src.domains.checkers.variation import Variation
from src.domains.checkers.parser import CheckersParser
from src.domains.checkers.piece import Piece

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

    # Clear board
    for square in king_state.pieces.position:
        king_state.pieces.position[square] = None

    # Place a red king
    king_state.pieces.position[29] = Piece(
        "red",
        king=True
    )

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

    promotion_state = GameState()

    piece = promotion_state.pieces.piece_at(25)

    promotion_state.pieces.position[25] = None

    promotion_state.pieces.position[4] = piece

    promotion_state.check_promotion(
        piece,
        4
    )

    print(
        "Piece at square 4:",
        promotion_state.pieces.piece_at(4).symbol()
    )

    print()

    # ==========================
    # PROMOTION ANIMATION TEST
    # ==========================

    print("PROMOTION ANIMATION TEST")
    print("---------------------")

    promotion_game = GameState()

    # Clear board
    for square in promotion_game.pieces.position:
        promotion_game.pieces.position[square] = None

    # Place a normal red man
    promotion_game.pieces.position[25] = Piece(
        "red"
    )

    print(
        "Piece placed:",
        promotion_game.pieces.piece_at(25).symbol()
    )

    print()

    renderer = Renderer()

    parser = CheckersParser()

    move = parser.parse(
        "25-29"
    )

# ===== END OF PART 1 =====
# ===== PART 2 =====

    variation = Variation(
        "Promotion Animation",
        [
            move
        ]
    )

    player = VariationPlayer(
        promotion_game,
        renderer
    )

    player.play(
        variation
    )


if __name__ == "__main__":

    main()