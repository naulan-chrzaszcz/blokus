# How to create a Piece

This document explains how to create and store pieces using a series of coordinate sets. Each coordinate set defines the positions of the individual parts of the piece on a grid.

## Coordinate Format

Each piece is represented by a series of coordinate sets. The coordinates are formatted as `x,y`, where `x` is the horizontal position and `y` is the vertical position on the grid. The format uses specific separators to organize the data:

## Storing Pieces

To store pieces in your project, follow these steps:

1. **Create a Text File**: 
   - Navigate to the `/res/pieces` directory.
   - Create a new text file (e.g., `pieces.txt`).

2. **Store Data on One Line**:
   - Format the pieces as a single line of text in the file, using the coordinate format described earlier.
   - Example content for `piece.txt`:
     ```
     1,0;0,1;1,1;2,1&1,0;0,1;1,1;2,1;3,1&1,0;2,0;0,1;1,1;1,2
     ```

#### Separators

1. **Comma (`,`)**:
   - **Purpose**: Separates individual coordinate values within a single coordinate.
   - **Example**: In `1,0`, `1` is the x-value (horizontal position) and `0` is the y-value (vertical position).

2. **Semicolon (`;`)**:
   - **Purpose**: Separates multiple coordinates that belong to the same piece.
   - **Example**: In the string `1,0;0,1;1,1;2,1`, each coordinate `1,0`, `0,1`, `1,1`, and `2,1` is part of the same piece.

3. **Ampersand (`&`)**:
   - **Purpose**: Separates different pieces from each other.
   - **Example**: In `1,0;0,1;1,1;2,1&1,0;0,1;1,1;2,1;3,1`, the first piece is defined by `1,0;0,1;1,1;2,1`, while the second piece is defined by `1,0;0,1;1,1;2,1;3,1`.

