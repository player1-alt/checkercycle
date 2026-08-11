
from src.renderer.settings import SETTINGS


class Timeline:
    """
    Controls the fixed CheckerCycle timing.

    Each square receives:
    - 10 seconds of audio
    - 3 seconds of silence

    Total cycle per square = 13 seconds.
    """

    def __init__(self):

        self.audio_duration = SETTINGS["audio"]["square_duration"]
        self.move_pause = SETTINGS["audio"]["move_pause"]

        self.square_cycle = (
            self.audio_duration
            + self.move_pause
        )

    def audio_time(self):
        """
        How long the MP3 for a square plays.
        """

        return self.audio_duration

    def pause_time(self):
        """
        How long the board waits after the MP3
        before the piece moves.
        """

        return self.move_pause

    def square_duration(self):
        """
        Total time occupied by one square:

        audio + pause
        """

        return self.square_cycle
