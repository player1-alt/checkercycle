from src.renderer.settings import SETTINGS


class Timeline:
    """
    Controls timing for replay, animation, and audio.
    """


    def __init__(self):

        self.base_interval = SETTINGS["timeline"]["base_interval"]
        self.start_hold = SETTINGS["timeline"]["start_hold"]
        self.hold_increase = SETTINGS["timeline"]["hold_increase"]



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
        """

        return self.move_duration(
            move_number,
            total_moves
        )



    def hold_time(self, move_number, total_moves):
        """
        Returns pause duration before a move.

        Gets longer as the variation progresses.
        """

        progress = move_number / max(total_moves, 1)

        hold = self.start_hold + (
            progress * self.hold_increase
        )

        return round(hold, 2)