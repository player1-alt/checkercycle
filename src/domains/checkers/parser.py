from .move import Move


class CheckersParser:
    """
    Converts checkers notation into Move objects.
    """

    def parse(self, notation):
        try:
            parts = notation.split("-")

            from_square = int(parts[0])
            to_square = int(parts[1])

            return Move(from_square, to_square)

        except Exception:
            print("Invalid checkers notation.")
            return None