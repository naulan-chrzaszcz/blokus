import unittest

from src.exceptions import *
from src.board import Board
from src.colors import Colors
from src.piece import Piece
from src.player import Player


class PlayerTest(unittest.TestCase):

    def test_get_piece(self) -> None:
        piece = Piece(tuple([(0, 0)]))
        player = Player(Colors.BLUE, [piece])

        with self.assertRaises(PieceNotFoundException):
            player.get_piece(-1)

        with self.assertRaises(PieceNotFoundException):
            player.get_piece(1)

        piece_from_get = player.get_piece(0)
        self.assertEqual(piece, piece_from_get)

    def test_place_piece(self) -> None:
        player_blue = Player(Colors.BLUE, [Piece(tuple([(0, 0), (1, 0)])) for _ in range(21)])
        board = Board(5, 5)
        board.save()
        piece = player_blue.get_piece(0)

        with self.assertRaises(PieceNotInCornerException):
            player_blue.place_piece(board, piece, 5, 5)

        player_blue.place_piece(board, piece, 0, 0)
        self.assertEqual(20, len(player_blue.deck))
        piece = player_blue.get_piece(0)

        board.save()
        with self.assertRaises(PieceOverlapException):
            player_blue.place_piece(board, piece, 0, 0)

        with self.assertRaises(NotAdjacentPieceException):
            player_blue.place_piece(board, piece, 3, 3)

        board.display()
        player_blue.place_piece(board, piece, 2, 1)
        
        player_red = Player(Colors.RED, [Piece(tuple([(0, 0), (1, 0)])) for _ in range(21)])
        piece = player_red.get_piece(0)
        
        board.restore()
        
        piece = player_blue.get_piece(0)
        player_blue.place_piece(board, piece, 1, 1)
        board.display()
        
