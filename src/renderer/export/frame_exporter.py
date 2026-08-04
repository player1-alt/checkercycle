from PIL import Image, ImageDraw


class FrameExporter:
    """
    Exports a checkerboard as a PNG image.
    """

    def __init__(self):

        self.square_size = 100
        self.board_size = 8

        self.image_size = (
            self.square_size * self.board_size
        )

        # Colors
        self.light_square = (240, 217, 181)
        self.dark_square = (0, 0, 0)


    def export(self, filename="frame0001.png"):

        image = Image.new(
            "RGB",
            (self.image_size, self.image_size),
            self.light_square
        )

        draw = ImageDraw.Draw(image)

        for row in range(self.board_size):

            for column in range(self.board_size):

                if (row + column) % 2 == 1:

                    left = column * self.square_size
                    top = row * self.square_size

                    right = left + self.square_size
                    bottom = top + self.square_size

                    draw.rectangle(
                        [
                            (left, top),
                            (right, bottom)
                        ],
                        fill=self.dark_square
                    )

        image.save(filename)

        print(f"Saved {filename}")