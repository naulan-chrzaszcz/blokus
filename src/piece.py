from typing import Generator, List, Tuple
from .colors import Colors

class Piece:
    """Represents a game piece using a set of coordinates.

    The piece is defined by a tuple of coordinates that represent its cells.
    """
    MAX_SIZE: int = 5
    data: Tuple[Tuple[int, int]]
    color: Colors

    bottom_left = None
    bottom_right = None
    top_left = None
    top_right = None

    def __init__(self, data: Tuple[Tuple[int, int]]) -> None:
        """Create a new Piece

        Args:
            data (tuple): A tuple of coordinates representing the cells of the piece,
                          where each coordinate is a tuple of (x, y).
        """
        self.data = data
        self.__get_extremities()

    def iterate_data(self) -> Generator[Tuple[int, int], None, None]:
        """Yields the coordinates of each cell in the piece.

        Yields:
            tuple: A tuple containing (cell_x, cell_y) for each cell in the piece.
        """
        for cell_x, cell_y in self.data:
            yield (cell_x, cell_y)

    def rotate(self) -> None:
        """Rotates the piece by 90 degrees clockwise."""
        min_x = min(x for x, _ in self.data)
        min_y = min(y for _, y in self.data)

        cx = min_x + (max(x for x, _ in self.data) - min_x) // 2
        cy = min_y + (max(y for _, y in self.data) - min_y) // 2

        rotated_piece = [((y - cy) + cx, cy - (x - cx)) for x, y in self.data]
        self.data = tuple([(x - min(x for x, _ in rotated_piece),
                            y - min(y for _, y in rotated_piece)) for x, y in rotated_piece])
        
        self.__get_extremities()

    def mirror(self, horizontal: bool = True, vertical: bool = True) -> None:
        """Mirrors the piece horizontally and/or vertically."""
        min_x = min(x for x, _ in self.data)
        max_x = max(x for x, _ in self.data)
        min_y = min(y for _, y in self.data)
        max_y = max(y for _, y in self.data)

        mirrored_piece = []
        if horizontal:
            cx = (min_x + max_x) // 2

            for x, y in self.data:
                mirrored_piece.append(((cx - (x - cx)), y))

        if vertical:
            cy = (min_y + max_y) // 2

            for x, y in (mirrored_piece if horizontal else self.data):
                mirrored_piece.append((x, (cy - (y - cy))))

        self.data = tuple([(x - min(x for x, _ in mirrored_piece),
                            y - min(y for _, y in mirrored_piece)) for x, y in mirrored_piece])
        
        self.__get_extremities()

    def __get_extremities(self) -> None:
        for cell_x, cell_y in self.iterate_data():
            if (self.data.count((cell_x - 1, cell_y)) == 0
                and self.data.count((cell_x, cell_y - 1)) == 0):
                self.top_left = (cell_x, cell_y)
            if (self.data.count((cell_x, cell_y - 1)) == 0
                and self.data.count((cell_x + 1, cell_y)) == 0):
                self.top_right = (cell_x, cell_y)
            if (self.data.count((cell_x - 1, cell_y)) == 0
                and self.data.count((cell_x, cell_y + 1)) == 0):
                self.bottom_left = (cell_x, cell_y)
            if (self.data.count((cell_x + 1, cell_y)) == 0
                and self.data.count((cell_x, cell_y + 1)) == 0):
                self.bottom_right = (cell_x, cell_y)

    def set_color(self, color: Colors) -> None:
        self.color = color
    
    def get_color(self) -> Colors:
        return self.color

