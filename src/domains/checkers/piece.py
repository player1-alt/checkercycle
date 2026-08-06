class Piece:
    """
    Represents a checker piece.
    """

    def __init__(self, color, king=False):

        self.color = color
        self.king = king


    def promote(self):

        self.king = True


    def symbol(self):

        if self.king:

            if self.color == "red":
                return "R♛"

            else:
                return "W♛"


        else:

            if self.color == "red":
                return "R"

            else:
                return "W"