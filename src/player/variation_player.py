import time


class VariationPlayer:
    """
    Plays a checkers variation move by move.
    """

    def __init__(self, game_state, renderer, interval=2):
        self.game_state = game_state
        self.renderer = renderer
        self.interval = interval

    def play(self, variation):

        print(f"Playing: {variation.name}")
        print()

        for move in variation.moves:

            print(f"Applying move: {move}")

            self.game_state.apply_move(move)

            self.renderer.render(self.game_state, move)

            print()

            time.sleep(self.interval)