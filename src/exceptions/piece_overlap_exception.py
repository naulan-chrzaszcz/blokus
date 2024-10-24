

class PieceOverlapException(Exception):
    def __init__(self):
        super().__init__("The piece is overlapping with another piece on the board.")

