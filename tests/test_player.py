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
        player = Player(Colors.BLUE, [Piece(tuple([(0, 0)])) for _ in range(21)])
        board = Board(5, 5)
        board.save()
        piece = player.get_piece(0)

        with self.assertRaises(PieceNotInCornerException):
            player.place_piece(board, piece, 5, 5)

        player.place_piece(board, piece, 0, 0)
        piece = player.get_piece(0)

        board.save()
        with self.assertRaises(PieceOverlapException):
            player.place_piece(board, piece, 0, 0)

        with self.assertRaises(NotAdjacentPieceException):
            player.place_piece(board, piece, 2, 2)

        player.place_piece(board, piece, 1, 1)
