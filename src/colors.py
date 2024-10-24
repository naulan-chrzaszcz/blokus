from enum import Enum, unique


@unique
class Colors(Enum):
    """An Enum class that stores and manages information about colors.

    Each enumeration associates a unique **COLOR_NAME** with a corresponding **ID**, 
    formatted as: `COLOR_NAME = ID`.

    This structure promotes consistency and simplifies the management of color-related functionality, 
    such as rendering colors in display settings or terminal output.

    ### Details:
    - The **COLOR_NAME** must be unique, as it represents a specific color.
    - The **ID** must also be unique, as it is used by the board to identify and display the correct color.

    ### Adding Colors:
    When adding a new color, you must also update the `__str__()` method. 
    This ensures that the **ID** is correctly mapped to a string, 
    allowing the terminal to render the block with the corresponding color.

    Raises:
        Exception: If either the **COLOR_NAME** or **ID** is not unique, 
                   or if there is an error during the color-to-string mapping.
    """
    RESET = 0
    
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    LIGHT_GRAY = 6

    def __str__(self) -> str:
        """Converts the current color enumeration to its corresponding terminal color code string.

        This method maps the color ID (self.value) to the corresponding ANSI escape code for terminal output.
        If the ID does not match any predefined colors, an exception is raised.

        Raises:
            Exception: If the color ID is not found in the predefined mappings.

        Returns:
            str: ANSI escape code representing the terminal color corresponding to the color ID.
        """
        match self.value:
            case self.RESET.value:
                return '\033[0m'
            case self.RED.value:
                return '\033[31m'
            case self.GREEN.value:
                return '\033[32m'
            case self.YELLOW.value:
                return '\033[33m'
            case self.BLUE.value:
                return '\033[34m'
            case self.MAGENTA.value:
                return '\033[35m'
            case self.LIGHT_GRAY.value:
                return '\033[37m'
            case _:
                raise Exception(f"The Colors value {self.value} is not referenced in __str__().")
