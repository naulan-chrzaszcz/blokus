import unittest

from src.exceptions import *
from src.board import Board
from src.colors import Colors
from src.piece import Piece


class BoardTest(unittest.TestCase):
    WIDTH: int = 5
    HEIGHT: int = 5

    def setUp(self) -> None:
        self.board = Board(self.WIDTH, self.HEIGHT)

    def test_is_piece_overlapping_at(self) -> None:
        piece = Piece(tuple([(0, 0)]))
        piece.set_color(Colors.BLUE)

        self.board.put(piece, 2, 2)
        # Needed to call 'save' method to have 'backup' 
        # variable used in the 'is_piece_overlapping_at' method
        self.board.save()

        self.assertFalse(self.board.is_piece_overlapping_at(piece, 0, 0))
        self.assertFalse(self.board.is_piece_overlapping_at(piece, -1, -1))
        self.assertTrue(self.board.is_piece_overlapping_at(piece, 2, 2))

    def test_is_piece_corner_at(self) -> None:
        piece = Piece(tuple([(0, 0)]))

        self.assertFalse(self.board.is_piece_in_corner_at(piece, 2, 2))
        self.assertFalse(self.board.is_piece_in_corner_at(piece, -1, -1))
        self.assertTrue(self.board.is_piece_in_corner_at(piece, 0, 0))
        self.assertTrue(self.board.is_piece_in_corner_at(piece, 0, self.HEIGHT - 1))
        self.assertTrue(self.board.is_piece_in_corner_at(piece, self.WIDTH - 1, 0))
        self.assertTrue(self.board.is_piece_in_corner_at(piece, self.WIDTH - 1, self.HEIGHT - 1))

    def test_can_place_piece_at(self) -> None:
        piece = Piece(tuple([(0, 0)]))
        piece.set_color(Colors.BLUE)
        
        self.board.put(piece, 2, 2)
        # Needed to call 'save' method to have 'backup' 
        # variable used in the 'can_place_piece_at' method
        self.board.save()

        with self.assertRaises(OutOfBoardException):
            self.board.can_place_piece_at(piece, -1, -1)

        with self.assertRaises(PieceOverlapException):
            self.board.can_place_piece_at(piece, 2, 2)

        with self.assertRaises(NotAdjacentPieceException):
            self.board.can_place_piece_at(piece, 0, 0)

        with self.assertRaises(NotAdjacentPieceException):
            self.board.can_place_piece_at(piece, 2, 1)

        with self.assertRaises(NotAdjacentPieceException):
            self.board.can_place_piece_at(piece, 1, 2)

        with self.assertRaises(NotAdjacentPieceException):
            self.board.can_place_piece_at(piece, 2, 3)

        with self.assertRaises(NotAdjacentPieceException):
            self.board.can_place_piece_at(piece, 3, 2)

        self.board.can_place_piece_at(piece, 1, 1)
        self.board.can_place_piece_at(piece, 1, 3)
        self.board.can_place_piece_at(piece, 3, 3)
        self.board.can_place_piece_at(piece, 3, 1)
