from typing import List

from .exceptions import PieceNotFoundException, PieceNotInCornerException, PieceOverlapException
from .board import Board
from .piece import Piece
from .colors import Colors


class Player:
    """_summary_
    """
    # The color of the player and the piece that will be placed
    color: Colors
    # The deck contains 21 pieces at the initialization
    deck: List[Piece]

    def __init__(
        self,
        color: Colors,
        pieces: List[Piece],
    ) -> None:
        """Create a new Player

        Args:
            color (Colors): The color of the player and the piece that will be placed
            pieces (List[np.ndarray]): The deck contains 12 pieces at the initialization
        """
        self.color = color
        self.deck = pieces.copy()

    def get_piece(self, i: int) -> Piece:
        """_summary_

        Args:
            i (int): _description_

        Raises:
            PieceNotFoundException: _description_

        Returns:
            Piece: _description_
        """
        if i < 0 or i >= len(self.deck):
            raise PieceNotFoundException()
        return self.deck[i]

    def place_piece(self, board: Board, piece: Piece, x: int, y: int) -> None:
        """_summary_

        Args:
            board (Board): _description_
            piece (Piece): _description_
            x (int): _description_
            y (int): _description_

        Raises:
            PieceNotFoundException: _description_
            NotAdjacentPieceException: _description_
            PieceInCornerException: _description_
            PieceOverlapException: _description_
        """
        if len(self.deck) == 21:
            if not board.is_piece_in_corner_at(piece, x, y):
                raise PieceNotInCornerException()
            elif board.is_piece_overlapping_at(piece, x, y):
                raise PieceOverlapException()

        if len(self.deck) < 21:
            board.can_place_piece_at(piece, x, y)
        board.put(piece, self.color, x, y)

    def display_deck(self) -> None:
        """_summary_
        """
        pieces_to_display = [[[0 for _ in range(Piece.MAX_SIZE)] for _ in range(Piece.MAX_SIZE)] for _ in range(len(self.deck))]
        
        i = 0
        while i < len(self.deck):
            piece = self.deck[i].data            
            for x, y in piece:
                pieces_to_display[i][y][x] = 1
            i += 1

        for y in range(Piece.MAX_SIZE):
            line = " | "
            for piece_to_display in pieces_to_display:
                for x in range(Piece.MAX_SIZE):
                    if piece_to_display[y][x] == 1:
                        line += f"{str(self.color)}■{str(Colors.RESET)}"
                    else:
                        line += " "
                line += " | "
            print(line)
