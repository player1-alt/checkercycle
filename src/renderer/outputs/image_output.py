from PIL import Image, ImageDraw
from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Creates board images and animation frames.
    """


    def __init__(self):

        self.frame_counter = 1
        self.square_mapper = SquareMapper()



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
                        fill=(80,80,80)
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
                center_x-radius,
                center_y-radius,
                center_x+radius,
                center_y+radius
            ],
            fill=colour,
            outline="black"
        )



    def display(self, game_state):

        size = 640


        image = Image.new(
            "RGB",
            (size,size),
            "white"
        )


        draw = ImageDraw.Draw(image)


        self.draw_board(draw)


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
        game_state,
        moving_square,
        position
    ):


        size = 640


        image = Image.new(
            "RGB",
            (size,size),
            "white"
        )


        draw = ImageDraw.Draw(image)


        self.draw_board(draw)



        # draw all pieces except moving piece

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
                    colour
                )



        # draw moving piece at animation position

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
                colour
            )



        filename = (
            f"animation{self.frame_counter:04}.png"
        )


        image.save(filename)


        print(
            f"Saved animation frame {filename}"
        )


        self.frame_counter += 1