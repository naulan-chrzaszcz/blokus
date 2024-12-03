import unittest

from src.exceptions import PieceNotFoundException, NotEnoughPiecesInTheDeckException
from src.piece import Piece
from src.player.deck import Deck

from .player.test_deck import TestDeck


class DeckTest(unittest.TestCase):

    def test_create(self) -> None:
        with self.assertRaises(NotEnoughPiecesInTheDeckException):
            Deck([(0, 0) for _ in range(Deck.MAX_SIZE + 1)])
        with self.assertRaises(NotEnoughPiecesInTheDeckException):
            Deck([(0, 0) for _ in range(Deck.MAX_SIZE - 1)])
        Deck([(0, 0) for _ in range(Deck.MAX_SIZE)])

    def test_get(self) -> None:
        piece = Piece(tuple([(0, 0)]))
        deck = TestDeck([piece])

        with self.assertRaises(PieceNotFoundException):
            deck.get(-1)
        with self.assertRaises(PieceNotFoundException):
            deck.get(1)
        self.assertEqual(piece, deck.get(0))
