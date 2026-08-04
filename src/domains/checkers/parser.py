from .move import Move


class CheckersParser:
    """
    Converts checkers notation into Move objects.

    Supports:
    11-15
    23x16x7|19,11
    """


    def parse(self, notation):

        try:

            notation = notation.strip()


            # Capture move
            if "x" in notation:

                parts = notation.split("|")


                path_text = parts[0]

                path = [
                    int(square)
                    for square in path_text.split("x")
                ]


                captured_squares = []


                if len(parts) > 1:

                    captured_squares = [
                        int(square)
                        for square in parts[1].split(",")
                    ]


                return Move(
                    path,
                    is_capture=True,
                    captured_squares=captured_squares
                )


            # Normal move
            if "-" in notation:

                path = [
                    int(square)
                    for square in notation.split("-")
                ]


                return Move(
                    path
                )


            print("Unknown notation.")
            return None


        except Exception:

            print("Invalid checkers notation.")
            return None