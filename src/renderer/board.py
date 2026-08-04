class Board:

    def __init__(self):
        self.squares = []

        for row in range(8):

            current_row = []

            for column in range(8):

                if (row + column) % 2 == 0:
                    current_row.append("w")
                else:
                    current_row.append("b")

            self.squares.append(current_row)

    def display(self):

        print()

        for row in self.squares:

            print(" ".join(row))

        print()