from PIL import Image, ImageDraw
from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Saves board images and animation frames.
    """

    def __init__(self):
        self.frame_counter = 1
        self.square_mapper = SquareMapper()


    def draw_board(self, draw):

        size = 640
        square_size = size // 8

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


    def draw_piece(
        self,
        draw,
        row,
        column,
        colour
    ):

        size = 640
        square_size = size // 8

        center_x = (
            column * square_size
            + square_size // 2
        )

        center_y = (
            row * square_size
            + square_size // 2
        )

        radius = square_size // 3


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


    def display(self, game_state):

        size = 640

        image = Image.new(
            "RGB",
            (size, size),
            "white"
        )

        draw = ImageDraw.Draw(image)


        self.draw_board(draw)


        # Draw existing pieces
        for square, piece in game_state.pieces.position.items():

            if piece is not None:

                row, column = self.square_mapper.coordinates(
                    square
                )


                if piece.color == "red":
                    colour = "red"
                else:
                    colour = "white"


                self.draw_piece(
                    draw,
                    row,
                    column,
                    colour
                )


        filename = f"frame{self.frame_counter:04}.png"

        image.save(filename)

        print(
            f"IMAGE OUTPUT: Saved {filename}"
        )

        self.frame_counter += 1



    def save_animation_frame(
        self,
        position
    ):

        size = 640

        image = Image.new(
            "RGB",
            (size, size),
            "white"
        )

        draw = ImageDraw.Draw(image)


        self.draw_board(draw)


        row, column = position


        self.draw_piece(
            draw,
            row,
            column,
            "red"
        )


        filename = (
            f"animation{self.frame_counter:04}.png"
        )


        image.save(filename)

        print(
            f"Saved animation frame {filename}"
        )

        self.frame_counter += 1