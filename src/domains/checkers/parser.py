from .move import Move


class CheckersParser:
    """
    Converts renderer instructions into Move objects.
    """

    def parse(self, notation):

        try:

            captured_squares = []

            # Separate movement and captures
            if "|" in notation:

                movement, captures = notation.split("|")

                captured_squares = [
                    int(square)
                    for square in captures.split(",")
                ]

            else:

                movement = notation


            # Build path
            separator = "-"

            squares = movement.split(separator)

            path = [
                int(square)
                for square in squares
            ]


            return Move(
                path,
                captured_squares=captured_squares
            )


        except Exception:

            print("Invalid renderer notation.")
            return None