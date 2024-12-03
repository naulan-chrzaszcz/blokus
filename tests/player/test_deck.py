from copy import copy
from typing import List

from src.piece import Piece
from src.player.deck import Deck


class TestDeck(Deck):
    def __init__(self, pieces: List[Piece]) -> None:
        self.pieces = [copy(piece) for piece in pieces]
        self.index = 0
