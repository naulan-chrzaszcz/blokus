

class PieceNotFoundException(Exception):
    def __init__(self):
        super().__init__("The piece selected doesn't exist.")
