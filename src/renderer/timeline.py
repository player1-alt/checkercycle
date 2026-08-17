from src.renderer.settings import SETTINGS


class Timeline:
    """
    Controls CheckerCycle timing modes.

    Three timing modes are available:

    13 seconds
    8 seconds
    4 seconds

    The same timing values can be used independently
    by slideshow and audio outputs.
    """

    def __init__(self):

        self.mode_13 = SETTINGS["timing"]["mode_13"]
        self.mode_8 = SETTINGS["timing"]["mode_8"]
        self.mode_4 = SETTINGS["timing"]["mode_4"]

        self.transition = SETTINGS["timing"]["transition"]


    def duration(self, mode):
        """
        Return the duration for the selected mode.
        """

        if mode == 13:
            return self.mode_13

        if mode == 8:
            return self.mode_8

        if mode == 4:
            return self.mode_4

        raise ValueError(
            f"Unknown timeline mode: {mode}"
        )


    def transition_duration(self):
        """
        Return the slideshow transition duration.
        """

        return self.transition