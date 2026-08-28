from PIL import Image, ImageDraw, ImageFont

from src.domains.checkers.square_mapper import SquareMapper


class ImageOutput:
    """
    Creates board images and animation frames.

    Each checker displays its permanent piece name.
    The name follows the piece as it moves.
    """

    def __init__(self):

        self.square_mapper = SquareMapper()

        self.frame_counter = 1

        self.saved_frames = []


        # Base font
        try:

            self.font_path = "arial.ttf"

        except:

            self.font_path = None



    def get_piece_font(
        self,
        draw,
        name,
        max_width
    ):

        """
        Automatically chooses a font size that fits
        the permanent piece name inside the checker.
        """

        # Start reasonably large
        size = 14


        while size >= 6:

            try:

                font = ImageFont.truetype(
                    self.font_path,
                    size
                )

            except:

                font = ImageFont.load_default()


            bbox = draw.textbbox(
                (0, 0),
                name,
                font=font
            )


            width = bbox[2] - bbox[0]


            if width <= max_width:

                return font


            size -= 1


        try:

            return ImageFont.truetype(
                self.font_path,
                6
            )

        except:

            return ImageFont.load_default()



    def reset(self):

        self.frame_counter = 1

        self.saved_frames = []

        print("IMAGE OUTPUT RESET")



    def draw_board(
        self,
        draw
    ):

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



    def draw_square_labels(
        self,
        draw
    ):

        size = 640
        square_size = size // 8


        for square in range(1, 33):

            row, column = (
                self.square_mapper.coordinates(
                    square
                )
            )


            x = column * square_size + 3
            y = row * square_size + 3


            colour = (
                "yellow"
                if (row + column) % 2 == 1
                else "black"
            )


            draw.text(
                (x, y),
                str(square),
                fill=colour,
                font=ImageFont.load_default()
            )



    def draw_piece(
        self,
        draw,
        row,
        column,
        colour,
        name,
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


        # ==========================
        # DRAW CHECKER
        # ==========================

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


        # ==========================
        # PIECE NAME
        # ==========================

        display_name = name


        # Add king marker
        if king:

            display_name = f"{name}♛"


        # Available width inside checker
        max_width = (
            radius * 2
            - 8
        )


        font = self.get_piece_font(
            draw,
            display_name,
            max_width
        )


        bbox = draw.textbbox(
            (0, 0),
            display_name,
            font=font
        )


        text_width = (
            bbox[2] - bbox[0]
        )


        text_height = (
            bbox[3] - bbox[1]
        )


        text_x = (
            center_x
            - text_width // 2
        )


        text_y = (
            center_y
            - text_height // 2
            - bbox[1]
        )


        # Black text on white pieces,
        # white text on red pieces
        text_colour = (
            "black"
            if colour == "white"
            else "white"
        )


        draw.text(
            (
                text_x,
                text_y
            ),
            display_name,
            fill=text_colour,
            font=font
        )



    def draw_position(
        self,
        draw,
        game_state
    ):

        for square, piece in (
            game_state.pieces.position.items()
        ):

            if piece is None:
                continue


            row, column = (
                self.square_mapper.coordinates(
                    square
                )
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
                piece.name,
                piece.king
            )



    def display(
        self,
        game_state
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
            (size, size),
            "white"
        )


        draw = ImageDraw.Draw(image)


        self.draw_board(draw)

        self.draw_square_labels(draw)


        # ==========================
        # FIND MOVING PIECE
        # ==========================

        moving_piece = (
            game_state.pieces.position.get(
                moving_square
            )
        )


        # ==========================
        # DRAW OTHER PIECES
        # ==========================

        for square, piece in (
            game_state.pieces.position.items()
        ):

            if square == moving_square:
                continue


            if piece is None:
                continue


            row, column = (
                self.square_mapper.coordinates(
                    square
                )
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
                piece.name,
                piece.king
            )


        # ==========================
        # DRAW MOVING PIECE
        # ==========================

        if moving_piece is not None:

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
                moving_piece.name,
                moving_piece.king
            )


        else:

            print(
                "WARNING: Missing moving piece:",
                moving_square
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