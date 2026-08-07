from PIL import Image, ImageDraw, ImageFont

from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Creates board images and animation frames.
    """


    def __init__(self):

        self.square_mapper = SquareMapper()

        self.frame_counter = 1

        self.saved_frames = []


        try:

            self.font = ImageFont.truetype(
                "arial.ttf",
                10
            )

        except:

            self.font = ImageFont.load_default()



    def reset(self):

        self.frame_counter = 1

        self.saved_frames = []

        print("IMAGE OUTPUT RESET")



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



    def draw_square_labels(self, draw):

        size = 640

        square_size = size // 8



        for square in range(1,33):


            row,column = (
                self.square_mapper.coordinates(square)
            )


            x = column * square_size + 3

            y = row * square_size + 3



            colour = (
                "yellow"
                if (row + column) % 2 == 1
                else "black"
            )



            draw.text(
                (x,y),
                str(square),
                fill=colour,
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
                center_x-radius,
                center_y-radius,
                center_x+radius,
                center_y+radius
            ],
            fill=colour,
            outline="black"
        )



        if king:


            draw.text(
                (
                    center_x-8,
                    center_y-8
                ),
                "K",
                fill="gold",
                font=self.font
            )



    def draw_position(
        self,
        draw,
        game_state
    ):


        for square,piece in game_state.pieces.position.items():


            if piece:


                row,column = (
                    self.square_mapper.coordinates(square)
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



    def display(self, game_state):


        size = 640


        image = Image.new(
            "RGB",
            (size,size),
            "white"
        )


        draw = ImageDraw.Draw(image)



        self.draw_board(draw)

        self.draw_square_labels(draw)

        self.draw_position(
            draw,
            game_state
        )



        filename = (
            f"frame{self.frame_counter:04}.png"
        )



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
            (size,size),
            "white"
        )


        draw = ImageDraw.Draw(image)



        self.draw_board(draw)

        self.draw_square_labels(draw)



        moving_piece = None



        for square,piece in game_state.pieces.position.items():


            if square == moving_square:

                moving_piece = piece

                continue



            if piece:


                row,column = (
                    self.square_mapper.coordinates(square)
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


            row,column = position


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