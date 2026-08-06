from PIL import Image, ImageDraw, ImageFont
from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Creates board images and animation frames.
    """


    def __init__(self):

        self.frame_counter = 1
        self.square_mapper = SquareMapper()

        # Stores every saved frame in creation order
        self.saved_frames = []


        try:
            self.font = ImageFont.truetype(
                "arial.ttf",
                10
            )
        except:
            self.font = ImageFont.load_default()



    def draw_board(self, draw):

        size = 640
        square_size = size // 8

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



    def draw_square_labels(self, draw):

        size = 640
        square_size = size // 8


        for square in range(1, 33):

            row, column = self.square_mapper.coordinates(
                square
            )


            # Small corner mark
            x = column * square_size + 3
            y = row * square_size + 3


            # Yellow on playable dark squares
            # Black on light squares
            if (row + column) % 2 == 1:
                label_colour = "yellow"
            else:
                label_colour = "black"


            draw.text(
                (x, y),
                str(square),
                fill=label_colour,
                font=self.font
            )



    def draw_piece(
    self,
    draw,
    row,
    column,
    colour,
    king=False
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
        if king:

            # Crown base
            draw.rectangle(
                [
                    center_x - 14,
                    center_y - 8,
                    center_x + 14,
                    center_y - 3
                ],
                fill="gold",
                outline="black"
            )

            # Left point
            draw.polygon(
                [
                    (center_x - 14, center_y - 3),
                    (center_x - 8, center_y - 18),
                    (center_x - 2, center_y - 3)
                ],
                fill="gold",
                outline="black"
            )

            # Middle point
            draw.polygon(
                [
                    (center_x - 4, center_y - 3),
                    (center_x, center_y - 22),
                    (center_x + 4, center_y - 3)
                ],
                fill="gold",
                outline="black"
            )

            # Right point
            draw.polygon(
                [
                    (center_x + 2, center_y - 3),
                    (center_x + 8, center_y - 18),
                    (center_x + 14, center_y - 3)
                ],
                fill="gold",
                outline="black"
            )

            # Jewels
            draw.ellipse(
                [
                    center_x - 10,
                    center_y - 20,
                    center_x - 6,
                    center_y - 16
                ],
                fill="red"
            )

            draw.ellipse(
                [
                    center_x - 2,
                    center_y - 24,
                    center_x + 2,
                    center_y - 20
                ],
                fill="blue"
            )

            draw.ellipse(
                [
                    center_x + 6,
                    center_y - 20,
                    center_x + 10,
                    center_y - 16
                ],
                fill="green"
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

        self.draw_square_labels(draw)


        for square, piece in game_state.pieces.position.items():

            if piece:

                row, column = self.square_mapper.coordinates(
                    square
                )


                colour = (
                    "red"
                    if piece.color == "red"
                    else "white"
                )


                self.draw_piece(
    draw,
    row,
    column,
    colour,
    piece.king
)


        filename = f"frame{self.frame_counter:04}.png"


        image.save(filename)


        self.saved_frames.append(
            filename
        )


        print(
            f"IMAGE OUTPUT: Saved {filename}"
        )


        self.frame_counter += 1



    def save_animation_frame(
        self,
        game_state,
        moving_square,
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

        self.draw_square_labels(draw)


        moving_piece = None


        for square, piece in game_state.pieces.position.items():

            if square == moving_square:

                moving_piece = piece
                continue


            if piece:

                row, column = self.square_mapper.coordinates(
                    square
                )


                colour = (
                    "red"
                    if piece.color == "red"
                    else "white"
                )


                self.draw_piece(
    draw,
    row,
    column,
    colour,
    piece.king
)


        if moving_piece:

            row, column = position


            colour = (
                "red"
                if moving_piece.color == "red"
                else "white"
            )


            self.draw_piece(
    draw,
    row,
    column,
    colour,
    moving_piece.king
)


        filename = (
            f"animation{self.frame_counter:04}.png"
        )


        image.save(filename)


        self.saved_frames.append(
            filename
        )


        print(
            f"Saved animation frame {filename}"
        )


        self.frame_counter += 1