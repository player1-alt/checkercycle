from src.domains.checkers.game_state import GameState
from src.domains.checkers.move import Move
from src.domains.checkers.variation import Variation
from src.player.variation_player import VariationPlayer
from src.renderer.renderer import Renderer


def main():

    game_state = GameState()

    renderer = Renderer()

    variation = Variation(
        "Test Opening",
        [
            Move(11, 15),
            Move(23, 18),
            Move(8, 11)
        ]
    )

    player = VariationPlayer(
        game_state,
        renderer,
        interval=2
    )

    player.play(variation)


if __name__ == "__main__":
    main()