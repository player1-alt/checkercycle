import time


class VariationPlayer:

    def __init__(self, renderer, interval=2):
        self.renderer = renderer
        self.interval = interval

    def play(self, variation):
        print(f"Playing: {variation.name}")
        print()

        for move in variation.moves:
            self.renderer.render(move)
            time.sleep(self.interval)