class Piece:
    """
    Represents a checkers piece.
    """

    def __init__(self, color, king=False):

        self.color = color
        self.king = king


    def promote(self):

        self.king = True


    def is_king(self):

        return self.king


    def symbol(self):

        if self.king:

            if self.color == "red":
                return "RK"

            elif self.color == "white":
                return "WK"


        else:

            if self.color == "red":
                return "R"

            elif self.color == "white":
                return "W"


    def __str__(self):

        return self.symbol()