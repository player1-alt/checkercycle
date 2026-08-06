class SquareMapper:

    def __init__(self):

        self.mapping = {
             1:(0,1),  2:(0,3),  3:(0,5),  4:(0,7),
             5:(1,0),  6:(1,2),  7:(1,4),  8:(1,6),
             9:(2,1), 10:(2,3), 11:(2,5), 12:(2,7),
            13:(3,0), 14:(3,2), 15:(3,4), 16:(3,6),
            17:(4,1), 18:(4,3), 19:(4,5), 20:(4,7),
            21:(5,0), 22:(5,2), 23:(5,4), 24:(5,6),
            25:(6,1), 26:(6,3), 27:(6,5), 28:(6,7),
            29:(7,0), 30:(7,2), 31:(7,4), 32:(7,6),
        }

        self.reverse_mapping = {
            coordinates: square
            for square, coordinates in self.mapping.items()
        }

    def coordinates(self, square):
        return self.mapping[square]

    def square(self, row, column):
        return self.reverse_mapping[(row, column)]