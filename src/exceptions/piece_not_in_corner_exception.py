

class PieceNotInCornerException(Exception):
    def __init__(self, message="Piece cannot be placed in the corner of the board."):
        super().__init__(message)

