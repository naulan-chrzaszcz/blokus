

class NotEnoughPiecesInTheDeckException(Exception):
    def __init__(self) -> None:
        super().__init__("The deck must be contains 21 pieces.")
