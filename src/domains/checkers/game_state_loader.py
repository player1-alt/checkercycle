from src.domains.checkers.piece import Piece


class GameStateLoader:
    """
    Loads a board position into a GameState.
    """

    def load(self, game_state, position):

        # Clear the board
        for square in range(1, 33):
            game_state.pieces.position[square] = None

        # Place pieces
        for square, color in position.items():
            game_state.pieces.position[square] = Piece(color)