class Timeline:
    """
    Controls timing for replay, animation, and audio.
    """

    def __init__(self, base_interval=2):
        self.base_interval = base_interval


    def move_duration(self, move_number, total_moves):
        """
        Calculates how long a move sequence takes.

        Time gradually increases as the variation progresses.
        """

        progress = move_number / max(total_moves, 1)

        duration = self.base_interval + progress

        return round(duration, 2)



    def wait_time(self, move_number, total_moves):
        """
        Returns pause duration after a move.

        This is the thinking/memory time
        after the board changes.
        """

        return self.move_duration(
            move_number,
            total_moves
        )



    def hold_time(self, move_number, total_moves):
        """
        Returns pause duration before a move.

        Allows the learner to recognize
        the current board position before
        the next move happens.

        Later this can become:
        - beginner mode
        - master mode
        - blind mode
        - tournament mode
        """

        progress = move_number / max(total_moves, 1)

        # Starts at 3 seconds and slowly increases
        hold = 3 + (progress * 2)

        return round(hold, 2)