

class NotAdjacentPieceException(Exception):
    def __init__(self):
        super().__init__("The piece is not adjacent to the other piece on the board.")
