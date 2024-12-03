from typing import List

from ..exceptions import PieceNotInCornerException, PieceOverlapException
from ..board import Board
from ..piece import Piece
from ..colors import Colors
from .deck import Deck


class Player:
    """Represents a player in the game.

    The player has a specific color and a deck of pieces that can be used
    to place on the game board. The player can retrieve pieces from their deck 
    and place them on the board while adhering to the game's rules.
    """
    deck: Deck

    def __init__(self, color: Colors, pieces: List[Piece]) -> None:
        """Create a new Player

        Args:
            color (Colors): Color of the player and the piece that will be placed
            pieces (List[Piece]): Deck of pieces
        """
        self.deck = Deck(pieces)
        self.deck.apply_color(color)

    def place_piece(self, board: Board, piece: Piece, x: int, y: int) -> None:
        """Places a piece on the specified position on the board.

        This method checks if a piece can be placed at the given coordinates 
        based on game rules, including corner placement and overlap constraints.
        
        After being placed, the selected piece has been removed from the deck.

        Args:
            board (Board): Game board where the piece will be placed.
            piece (Piece): Piece to be placed on the board.
            x (int): x-coordinate on the board where the piece will be placed.
            y (int): y-coordinate on the board where the piece will be placed.

        Raises:
            PieceNotInCornerException: If the piece is being placed outside of the corner 
                                        when the deck contains 21 pieces.
            PieceOverlapException: If the piece overlaps with another piece on the board 
                                at the specified coordinates.
            NotAdjacentPieceException: If the piece being placed is not adjacent to 
                                    an existing piece (if applicable).
        """
        if self.deck.is_full():
            if board.is_piece_overlapping_at(piece, x, y):
                raise PieceOverlapException()
            if not board.is_piece_in_corner_at(piece, x, y):
                raise PieceNotInCornerException()
        else:
            board.can_place_piece_at(piece, x, y)
        board.put(piece, x, y)
        self.deck.remove(piece)
