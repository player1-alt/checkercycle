
class MoveEvent:
    """
    Represents everything that happens during one checker move.

    Every move occupies exactly one 13-second video slot.

    The narrator is independent of the 13-second timing.
    """

    def __init__(
        self,
        move,
        start_square,
        end_square,
        captured_squares,
        duration,
        hold,
        moving_piece
    ):

        self.move = move

        self.start_square = start_square

        self.end_square = end_square

        self.captured_squares = captured_squares

        # Duration of the movement itself.
        self.duration = duration

        # Position hold before the move.
        self.hold = hold

        # Fixed video interval.
        self.total_duration = 13.0

        # Complete decoded movement path.
        #
        # Examples:
        #
        # 9-13       -> [9, 13]
        # 27-11      -> [27, 11]
        # 23-16-7   -> [23, 16, 7]
        #
        self.path = list(move.path)

        # Snapshot of piece before board changes.
        self.moving_piece = moving_piece

        # Narrator text will be generated from path.
        self.narration_text = self._build_narration()

    def _number_word(self, number):

        words = {
            1: "ONE",
            2: "TWO",
            3: "THREE",
            4: "FOUR",
            5: "FIVE",
            6: "SIX",
            7: "SEVEN",
            8: "EIGHT",
            9: "NINE",
            10: "TEN",
            11: "ELEVEN",
            12: "TWELVE",
            13: "THIRTEEN",
            14: "FOURTEEN",
            15: "FIFTEEN",
            16: "SIXTEEN",
            17: "SEVENTEEN",
            18: "EIGHTEEN",
            19: "NINETEEN",
            20: "TWENTY",
            21: "TWENTY-ONE",
            22: "TWENTY-TWO",
            23: "TWENTY-THREE",
            24: "TWENTY-FOUR",
            25: "TWENTY-FIVE",
            26: "TWENTY-SIX",
            27: "TWENTY-SEVEN",
            28: "TWENTY-EIGHT",
            29: "TWENTY-NINE",
            30: "THIRTY",
            31: "THIRTY-ONE",
            32: "THIRTY-TWO"
        }

        return words.get(
            number,
            str(number)
        )

    def _build_narration(self):

        if not self.path:
            return ""

        words = []

        for square in self.path:

            words.append(
                self._number_word(square)
            )

        return " TO! ".join(words)

    def describe(self):

        print("MOVE EVENT")
        print("----------------")

        print(
            f"Move: {self.start_square}-"
            f"{self.end_square}"
        )

        print(
            f"Path: {self.path}"
        )

        print(
            f"Narrator: "
            f"{self.narration_text}"
        )

        if self.captured_squares:

            print(
                f"Captured: "
                f"{self.captured_squares}"
            )

        else:

            print(
                "No capture"
            )

        print(
            "Fixed move interval: 13.0s"
        )

