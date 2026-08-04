class Timeline:
    """
    Controls timing for replay, animation, and audio.
    """

    def __init__(self, base_interval=2):
        self.base_interval = base_interval


    def move_duration(self, move_number, total_moves):
        """
        Calculates how long a move should take.

        Later this can become:
        - opening speed
        - study speed
        - tournament speed
        - memory mode
        """

        progress = move_number / max(total_moves, 1)

        # Gradually increase time as the game progresses
        duration = self.base_interval + progress

        return round(duration, 2)


    def wait_time(self, move_number, total_moves):
        """
        Returns pause duration after a move.
        """

        return self.move_duration(move_number, total_moves)