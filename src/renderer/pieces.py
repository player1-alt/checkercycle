from src.domains.checkers.piece import Piece


class Pieces:

    PIECE_NAMES = {
        1: "Mash",
        2: "Eren",
        3: "Bojji",
        4: "Elric",
        5: "Naruto",
        6: "Sasuke",
        7: "Gojo",
        8: "Yuji",
        9: "Saitama",
        10: "Shinra",
        11: "Spike",
        12: "Asta",

        21: "Kal-El",
        22: "Scott",
        23: "Banshee",
        24: "Scofield",
        25: "Jon",
        26: "Suits",
        27: "Joey",
        28: "Rick",
        29: "Dex",
        30: "Ainz",
        31: "Coop",
        32: "Smith",
    }

    def __init__(self):

        self.position = {}

        # Black / Red
        for square in range(1, 13):

            self.position[square] = Piece(
                "red",
                self.PIECE_NAMES[square]
            )

        # Empty playable squares
        for square in range(13, 21):

            self.position[square] = None

        # White
        for square in range(21, 33):

            self.position[square] = Piece(
                "white",
                self.PIECE_NAMES[square]
            )

    def piece_at(self, square):

        return self.position[square]