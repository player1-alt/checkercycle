class BookLoader:

    def load(self, filename):
        with open(filename, "r") as file:
            return file.read()