class SquareLabels:
    """
    Draws checker square numbers on the board.
    """

    def __init__(self):

        self.enabled = True

        # Where the number appears
        self.position = "top-left"



    def draw(self, draw, coordinates, square):

        if not self.enabled:
            return


        row, col = coordinates


        offset_x = col * 80
        offset_y = row * 80


        if self.position == "top-left":

            x = offset_x + 5
            y = offset_y + 5

        elif self.position == "top-right":

            x = offset_x + 60
            y = offset_y + 5

        elif self.position == "bottom-left":

            x = offset_x + 5
            y = offset_y + 60

        else:

            x = offset_x + 60
            y = offset_y + 60



        draw.text(
            (x, y),
            str(square),
            fill="gray"
        )