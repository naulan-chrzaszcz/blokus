from copy import copy
from typing import List

from ..exceptions import PieceNotFoundException, NotEnoughPiecesInTheDeckException
from ..colors import Colors
from ..piece import Piece


class Deck:
    """Represents a collection of game pieces with a fixed maximum size."""
    MAX_SIZE: int = 21
    pieces: List[Piece]
    index: int

    def __init__(self, pieces: List[Piece]) -> None:
        """Initializes a new instance of the Deck.

        Args:
            pieces (List[Piece]): A list of pieces to populate the deck. 
                                  The deck must contain exactly 21 pieces at initialization.

        Raises:
            NotEnoughPiecesInTheDeckException: If fewer or more than 21 pieces are provided.
        """
        if (len(pieces) > self.MAX_SIZE
            or len(pieces) < self.MAX_SIZE):
            raise NotEnoughPiecesInTheDeckException()

        self.pieces = [copy(piece) for piece in pieces]
        self.index = 0

    def __iter__(self) -> List[Piece]:
        return self.pieces

    def __next__(self) -> Piece:
        if self.index >= self.size():
            raise StopIteration
        result = self.pieces[self.index]
        self.index += 1
        return result
    
    def apply_color(self, color: Colors) -> None:
        """Applies the given color to all pieces in the deck.

        Args:
            color (Colors): Color to apply to each piece in the deck.
        """
        for piece in self.pieces:
            piece.color = color

    def is_full(self) -> bool:
        """Checks if the deck is full.

        Returns:
            bool: True if the number of pieces in the deck equals the maximum size, False otherwise.
        """
        return self.size() == self.MAX_SIZE

    def size(self) -> int:
        """Retrieves the current number of pieces in the deck.

        Returns:
            int: The number of pieces in the deck.
        """
        return len(self.pieces)

    def display(self) -> None:
        """Displays the deck of pieces in a visual format."""
        # TODO: This code is not really optimized and does a lot of processing
        pieces_to_display = [[[0 for _ in range(Piece.MAX_SIZE)] for _ in range(Piece.MAX_SIZE)] for _ in range(self.size())]

        color = self.get(0).color
        for i, piece in enumerate(self.pieces):
            for x, y in piece.data:
                pieces_to_display[i][y][x] = 1

        for y in range(Piece.MAX_SIZE):
            line = " | "
            for piece_to_display in pieces_to_display:
                for x in range(Piece.MAX_SIZE):
                    if piece_to_display[y][x] == 1:
                        line += f"{str(color)}■{str(Colors.RESET)}"
                    else:
                        line += " "
                line += " | "
            print(line)

    def get(self, i: int) -> Piece:
        """Retrieves a piece from the deck at the specified index.

        Args:
            i (int): Index of the piece to retrieve from the deck.

        Raises:
            PieceNotFoundException: If the index is out of bounds (i.e., 
                                    less than 0 or greater than or equal to the deck size).

        Returns:
            Piece: Piece located at the specified index in the deck.
        """
        if i < 0 or i >= self.size():
            raise PieceNotFoundException()
        return self.pieces[i]
    
    def remove(self, piece: Piece) -> None:
        """Removes a specific piece from the deck.

        Args:
            piece (Piece): Piece to be removed from the deck.

        Raises:
            ValueError: If the specified piece is not found in the deck.
        """
        self.pieces.remove(piece)
