import unittest

from src.exceptions import *
from src.board import Board
from src.colors import Colors
from src.piece import Piece
from src.player import Player
from src.player.deck import Deck


class PlayerTest(unittest.TestCase):

    def test_place_piece(self) -> None:
        player_blue = Player(Colors.BLUE, [Piece(tuple([(0, 0), (1, 0)])) for _ in range(Deck.MAX_SIZE)])
        board = Board(5, 5)

        # Needed to call 'save' method to have 'backup' 
        # variable used in the 'can_place_piece_at' method.
        board.save()
        # Beginning of the game simulation.
        piece = player_blue.deck.get(0)
        with self.assertRaises(PieceNotInCornerException):
            player_blue.place_piece(board, piece, 3, 3)
        player_blue.place_piece(board, piece, 0, 0)
        self.assertEqual(20, player_blue.deck.size())

        # Corners detection test
        piece = player_blue.deck.get(0)
        board.save()
        with self.assertRaises(PieceOverlapException):
            player_blue.place_piece(board, piece, 0, 0)
        with self.assertRaises(NotAdjacentPieceException):
            player_blue.place_piece(board, piece, 3, 3)
        player_blue.place_piece(board, piece, 2, 1)
        self.assertEqual(19, player_blue.deck.size())

        # Verifies whether, in the presence of a piece of a different color, 
        # the pieces can be attached to each other and if collisions work correctly in this context.
        player_red = Player(Colors.RED, [Piece(tuple([(0, 0), (1, 0)])) for _ in range(Deck.MAX_SIZE)])
        piece = player_red.deck.get(0)
        board.save()
        player_red.place_piece(board, piece, 3, 4)
        self.assertEqual(20, player_red.deck.size())

        piece = player_red.deck.get(0)
        piece.rotate()
        board.save()
        player_red.place_piece(board, piece, 2, 2)
        self.assertEqual(19, player_red.deck.size())

        piece = player_red.deck.get(0)
        board.save()
        player_red.place_piece(board, piece, 0, 1)
        self.assertEqual(18, player_red.deck.size())
        board.display()
