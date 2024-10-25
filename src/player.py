from typing import List

from .exceptions import PieceNotFoundException, PieceNotInCornerException, PieceOverlapException
from .board import Board
from .piece import Piece
from .colors import Colors


class Player:
    """Represents a player in the game.

    The player has a specific color and a deck of pieces that can be used
    to place on the game board. The player can retrieve pieces from their deck 
    and place them on the board while adhering to the game's rules.
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
            pieces (List[Piece]): The deck contains 21 pieces at the initialization
        """
        self.color = color
        self.deck = pieces.copy()

    def get_piece(self, i: int) -> Piece:
        """Retrieves a piece from the deck at the specified index.

        This method returns the piece located at the given index in the deck.

        Args:
            i (int): The index of the piece to retrieve from the deck.

        Raises:
            PieceNotFoundException: If the index is out of bounds (i.e., 
                                    less than 0 or greater than or equal to the deck size).

        Returns:
            Piece: The piece located at the specified index in the deck.
        """
        if i < 0 or i >= len(self.deck):
            raise PieceNotFoundException()
        return self.deck[i]

    def place_piece(self, board: Board, piece: Piece, x: int, y: int) -> None:
        """Places a piece on the specified position on the board.

        This method checks if a piece can be placed at the given coordinates 
        based on game rules, including corner placement and overlap constraints.
        
        After being placed, the selected piece has been removed from the deck.

        Args:
            board (Board): The game board where the piece will be placed.
            piece (Piece): The piece to be placed on the board.
            x (int): The x-coordinate on the board where the piece will be placed.
            y (int): The y-coordinate on the board where the piece will be placed.

        Raises:
            PieceNotInCornerException: If the piece is being placed outside of the corner 
                                        when the deck contains 21 pieces.
            PieceOverlapException: If the piece overlaps with another piece on the board 
                                at the specified coordinates.
            NotAdjacentPieceException: If the piece being placed is not adjacent to 
                                    an existing piece (if applicable).
        """
        if len(self.deck) == 21:
            if not board.is_piece_in_corner_at(piece, x, y):
                raise PieceNotInCornerException()
            elif board.is_piece_overlapping_at(piece, x, y):
                raise PieceOverlapException()

        if len(self.deck) < 21:
            board.can_place_piece_at(piece, x, y)
        board.put(piece, self.color, x, y)
        self.deck.remove(piece)

    def display_deck(self) -> None:
        """Displays the player's deck of pieces in a visual format."""
        # TODO: This code is not really optimized and does a lot of processing
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
