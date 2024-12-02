import unittest

from src.piece import Piece

class PieceTest(unittest.TestCase):

    def test_get_extremities(self):
        rectangle_piece = Piece(((0, 0), (1, 0),
                                 (0, 1), (1, 1),
                                 (0, 2), (1, 2)))
        
        self.assertEqual([(0, 2)], rectangle_piece.bottom_left)
        self.assertEqual([(1, 2)], rectangle_piece.bottom_right)
        self.assertEqual([(0, 0)], rectangle_piece.top_left)
        self.assertEqual([(1, 0)], rectangle_piece.top_right)

        bar_piece = Piece(((0, 0), (1, 0), (2, 0)))

        self.assertEqual([(0, 0)], bar_piece.bottom_left)
        self.assertEqual([(0, 0)], bar_piece.top_left)
        self.assertEqual([(2, 0)], bar_piece.bottom_right)
        self.assertEqual([(2, 0)], bar_piece.top_right)

        bar_piece.rotate()

        self.assertEqual([(0, 0)], bar_piece.top_left)
        self.assertEqual([(0, 0)], bar_piece.top_right)
        self.assertEqual([(0, 2)], bar_piece.bottom_left)
        self.assertEqual([(0, 2)], bar_piece.bottom_right)

        point_piece = Piece(((0, 0), ))

        self.assertEqual([(0, 0)], point_piece.top_left)
        self.assertEqual([(0, 0)], point_piece.top_right)
        self.assertEqual([(0, 0)], point_piece.bottom_left)
        self.assertEqual([(0, 0)], point_piece.bottom_right)