from PIL import Image, ImageDraw
from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Saves the current board as a PNG image with pieces.
    """

    def __init__(self):
        self.frame_counter = 1
        self.square_mapper = SquareMapper()


    def display(self, game_state):

        size = 640
        square_size = size // 8

        image = Image.new(
            "RGB",
            (size, size),
            "white"
        )

        draw = ImageDraw.Draw(image)


        # Draw checkerboard
        for row in range(8):
            for column in range(8):

                if (row + column) % 2 == 1:

                    draw.rectangle(
                        [
                            column * square_size,
                            row * square_size,
                            (column + 1) * square_size,
                            (row + 1) * square_size
                        ],
                        fill=(80, 80, 80)
                    )


        # Draw pieces
        for square, piece in game_state.pieces.position.items():
            if piece is not None:

                row, column = self.square_mapper.coordinates(square)


                center_x = (
                    column * square_size
                    + square_size // 2
                )

                center_y = (
                    row * square_size
                    + square_size // 2
                )


                radius = square_size // 3


                # Determine piece colour from symbol
                symbol = piece.symbol()


                if symbol == "R":
                    colour = "red"
                else:
                    colour = "white"


                draw.ellipse(
                    [
                        center_x - radius,
                        center_y - radius,
                        center_x + radius,
                        center_y + radius
                    ],
                    fill=colour,
                    outline="black"
                )


        filename = f"frame{self.frame_counter:04}.png"

        image.save(filename)

        print(f"IMAGE OUTPUT: Saved {filename}")

        self.frame_counter += 1