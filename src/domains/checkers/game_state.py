from src.domains.checkers.piece import Piece
from src.domains.checkers.move import Move
from src.renderer.pieces import Pieces


class GameState:

    def __init__(self):
        self.pieces = Pieces()

    def apply_move(self, move):

        piece = self.pieces.piece_at(move.from_square)

        self.pieces.position[move.from_square] = None
        self.pieces.position[move.to_square] = piece