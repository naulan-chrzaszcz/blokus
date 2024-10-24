from typing import Generator, Tuple


class Piece:
    """Represents a game piece using a set of coordinates.

    The piece is defined by a tuple of coordinates that represent its cells.
    """
    MAX_SIZE: int = 5
    data: tuple

    def __init__(self, data: tuple) -> None:
        """Create a new Piece

        Args:
            data (tuple): A tuple of coordinates representing the cells of the piece,
                          where each coordinate is a tuple of (x, y).
        """
        self.data = data

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

