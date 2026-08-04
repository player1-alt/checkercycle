class Pieces:

    def __init__(self):

        self.position = {}

        # Black pieces

        for square in range(1, 13):
            self.position[square] = "B"

        # Empty playable squares

        for square in range(13, 21):
            self.position[square] = "."

        # White pieces

        for square in range(21, 33):
            self.position[square] = "W"

    def piece_at(self, square):

        return self.position[square]