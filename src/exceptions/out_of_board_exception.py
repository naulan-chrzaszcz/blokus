

class OutOfBoardException(Exception):
    def __init__(self):
        super().__init__("This piece is out of the board")
