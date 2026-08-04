class Piece:
    """
    Represents a single checkers piece.
    """

    def __init__(self, color):
        self.color = color
        self.king = False

    def promote(self):
        """
        Promote the piece to a king.
        """
        self.king = True

    def __str__(self):
        """
        Human-readable representation.
        """
        if self.king:
            return f"{self.color} king"
        
        return self.color

    def __repr__(self):
        """
        Developer-friendly representation.
        """
        return f"Piece(color='{self.color}', king={self.king})"