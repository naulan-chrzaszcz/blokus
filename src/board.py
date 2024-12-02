import numpy as np

from .exceptions import NotAdjacentPieceException, PieceOverlapException, OutOfBoardException
from .piece import Piece
from .colors import Colors


class Board:
    """Represents the game board where pieces are placed."""
    board: np.ndarray
    # Save of the board for specific context
    backup: np.ndarray
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        """Create a new Board

        Args:
            width (int): Width of the board.
            height (int): Height of the board.
        """
        self.width = width
        self.height = height
        self.board = np.array([[0 for _ in range(width)] for _ in range(height)])

    def put(self, piece: Piece, x: int, y: int) -> None:
        """Places a piece on the board at the specified coordinates.

        The piece will be represented with its designated color. 
        If there are already pieces in the target location, 
        the existing values will be overwritten with the new piece's value.

        Args:
            piece (Piece): Piece to be placed on the board.
            color (Colors): Color of the piece being placed.
            x (int): Horizontal coordinate where the piece will be placed.
            y (int): Vertical coordinate where the piece will be placed.
        """
        for x_piece, y_piece in piece.iterate_data():
            self.board[y_piece + y, x_piece + x] = 1 * piece.color.value

    def get(self) -> np.ndarray:
        """Returns the current state of the board.

        Returns:
            np.ndarray: NumPy array representing the current board.
        """
        return self.board

    def save(self) -> None:
        """Saves a backup of the current board state."""
        self.backup = self.board.copy()

    def restore(self) -> None:
        """Restores the board to the last saved state."""
        self.board[:] = self.backup

    def rotate(self) -> None:
        """Rotates the board 90 degrees counterclockwise."""
        self.board = np.rot90(self.board)

    def is_piece_in_corner_at(self, piece: Piece, x_offset: int, y_offset: int) -> bool:
        """Checks if any part of the piece is positioned in one of the corners of the board.

        Args:
            piece (Piece): Piece to check for corner placement.
            x (int): x-coordinate where the piece is intended to be placed.
            y (int): y-coordinate where the piece is intended to be placed.

        Returns:
            bool: True if at least one part of the piece is in a corner; otherwise, False.
        """
        i = 0
        while (i < len(piece.data) 
               and not ((y_offset + piece.data[i][1] == 0 and x_offset + piece.data[i][0] == 0)
                        or (y_offset + piece.data[i][1] == 0 and x_offset + piece.data[i][0] == (self.width - 1))
                        or (y_offset + piece.data[i][1] == (self.height - 1) and x_offset + piece.data[i][0] == 0)
                        or (y_offset + piece.data[i][1] == (self.height - 1) and x_offset + piece.data[i][0] == (self.width - 1)))):
            i += 1
        return i < len(piece.data)

    def is_piece_overlapping_at(self, piece: Piece, x_offset: int, y_offset: int) -> bool:
        """Checks if the given piece overlaps with existing pieces on the board.

        Args:
            piece (Piece): Piece to check.
            x_offset (int): Horizontal offset for placement.
            y_offset (int): Vertical offset for placement.

        Returns:
            bool: True if there is no overlap.
        """
        # TODO: Pour un utilisateur lambda, le self.backup ne doit pas être clair
        # et il ne faut pas oublier de faire une backup avant chaque previsualisation
        # 0: empty; 6: piece preview
        i = 0
        while i < len(piece.data) and self.backup[piece.data[i][1] + y_offset, piece.data[i][0] + x_offset] in [0, 6]:
            i += 1
        return i < len(piece.data)

    def can_place_piece_at(self, piece: Piece, x_offset: int, y_offset: int) -> None:
        """Verifies if the given piece can be placed at the specified coordinates on the board.

        This method checks for overlapping pieces and ensures that the piece
        is adjacent to at least one already placed piece on the board.

        Args:
            piece (Piece): Piece to be verified for placement.
            x_offset (int): Horizontal coordinate where the piece is intended to be placed.
            y_offset (int): Vertical coordinate where the piece is intended to be placed.

        Raises:
            NotAdjacentPieceException: When the piece is not adjacent to any other pieces on the board.
            PieceOverlapException: When the piece overlaps with another piece on the board.
            OutOfBoardException: When the piece coordinate is out of the board
        """
        for cell_x, cell_y in piece.iterate_data():
            cell_x += x_offset
            cell_y += y_offset
            if cell_x < 0 or cell_y < 0 or cell_x >= self.width or cell_y >= self.height:
                raise OutOfBoardException()

            if self.is_piece_overlapping_at(piece, x_offset, y_offset):
                raise PieceOverlapException()

        top_from = lambda tupl: (tupl[1] - 1) + y_offset
        right_from = lambda tupl: (tupl[0] + 1) + x_offset
        bottom_from = lambda tupl: (tupl[1] + 1) + y_offset
        left_from = lambda tupl: (tupl[0] - 1) + x_offset

        # TODO: Améliorer la lisibilité des conditions de detection de coins des pieces.
        for top_left in piece.top_left:
            if (top_from(top_left) >= 0 and left_from(top_left) >= 0
                and self.board[top_from(top_left), left_from(top_left)] == piece.color.value):

                if self.board[top_from(top_left), top_left[0] + x_offset] == piece.color.value:
                    raise NotAdjacentPieceException()
                if self.board[top_left[1] + y_offset, left_from(top_left)] == piece.color.value:
                    raise NotAdjacentPieceException()
                return

        for top_right in piece.top_right:
            if (top_from(top_right) >= 0 and right_from(top_right) < self.width
                and self.board[top_from(top_right), right_from(top_right)] == piece.color.value):

                if self.board[top_from(top_right), top_right[0] + x_offset] == piece.color.value:
                    raise NotAdjacentPieceException()
                if self.board[top_right[1] + y_offset, right_from(top_right)] == piece.color.value:
                    raise NotAdjacentPieceException()
                return

        for bottom_left in piece.bottom_left:
            if (bottom_from(bottom_left) < self.height and left_from(bottom_left) >= 0
                and self.board[bottom_from(bottom_left), left_from(bottom_left)] == piece.color.value):

                if self.board[bottom_from(bottom_left), bottom_left[0] + x_offset] == piece.color.value:
                    raise NotAdjacentPieceException()
                if self.board[bottom_left[1] + y_offset, left_from(bottom_left)] == piece.color.value:
                    raise NotAdjacentPieceException()
                return

        for bottom_right in piece.bottom_right:
            if (bottom_from(bottom_right) < self.height and right_from(bottom_right) < self.width
                and self.board[bottom_from(bottom_right), right_from(bottom_right)] == piece.color.value):
                
                if self.board[bottom_from(bottom_right), bottom_left[0] + x_offset] == piece.color.value:
                    raise NotAdjacentPieceException()
                if self.board[bottom_left[1] + y_offset, right_from(bottom_right)] == piece.color.value:
                    raise NotAdjacentPieceException()
                return
        raise NotAdjacentPieceException()

    def display(self) -> None:
        """Displays the current state of the board in the terminal.

        The display includes:
            - A border around the board.
            - Each piece is shown as a colored block.
            - Empty spaces are represented as blank spaces.
        """
        frame_str = f"{str(Colors.LIGHT_GRAY)}■"

        for y in range(-1, self.height + 1):
            line = ""
            for x in range(-1, self.width + 1):
                if x == -1:
                    line += frame_str
                    continue
                elif x == self.width:
                    line += frame_str
                    continue

                if y == -1 or y == self.height:
                    line += frame_str
                    continue

                cell = int(self.board[y, x])
                line += f"{str(Colors(cell))}■" if cell != 0 else f"{str(Colors.RESET)} "
            print(line)

