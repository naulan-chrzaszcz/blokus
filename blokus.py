import random
import time
import os

from typing import List

from src.exceptions import *
from src.piece import Piece
from src.board import Board
from src.player import Player
from src.colors import Colors


class Game:
    """Handles game setup, player management, and game flow."""
    # Colors available to attributes to Players
    PLAYERS_COLOR: List[Colors] = [Colors.BLUE, Colors.GREEN, Colors.RED, Colors.YELLOW]
    NUMBER_OF_PLAYERS: int = 4
    
    players: List[Player]
    pieces: List[Piece]
    board: Board

    def __init__(self, board: Board) -> None:
        """Create a new instance of the Game.

        Args:
            board (Board): The game board on which the game is played.
        """
        self.board = board
        
        self.players = []
        self.pieces = []
        self.__load_ressources()

        # Create and attribute color to player
        colors = self.PLAYERS_COLOR.copy()
        for _ in range(self.NUMBER_OF_PLAYERS):
            color = colors[random.randint(0, len(colors) - 1)]
            colors.remove(color)
            self.players.append(Player(color, self.pieces))

    def __load_ressources(self) -> None:
        """Loads chess piece data from text files in the 'res/pieces/' directory.

        Each file is read, and the data is processed into tuples of coordinates 
        for each piece, which are then stored in the `self.pieces` list.
        """
        pieces_path = "res/pieces/"
        piece_separator = "&"
        coord_piece_separator = ";"
        coord_separator = ","

        for root, _, files in os.walk(pieces_path):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file)) as piece_file:
                        for raw_data_piece in piece_file.read().split(piece_separator):
                            piece_data = []
                            for coord_piece in raw_data_piece.split(coord_piece_separator):
                                x, y = coord_piece.split(coord_separator)
                                piece_data.append((int(x), int(y)))
                            self.pieces.append(Piece(tuple(piece_data)))

    def screen_clear(self) -> None:
        """Clears the terminal screen."""
        os.system("clear")

    def run(self) -> None:
        """Main game loop that manages player turns and piece placement.

        Continuously displays the board and player options, allowing each 
        player to select and place pieces until the game is complete.
        """
        while True:
            i = 0
            while i < len(self.players):
                player = self.players[i]

                self.board.display()
                player.deck.display()

                print(f"{str(Colors.RESET)} Quel piece voulez-vous placer > ", end="")
                piece: Piece | None = None
                try:
                    piece = player.deck.get(int(input()) - 1)
                except ValueError:
                    print("Choix non valide")
                    continue
                except OutOfBoardException:
                    print("La piece n'existe pas")
                    continue
                except Exception as e:
                    print(e)

                self.screen_clear()
                self.board.display()

                player_input = ""
                self.board.save()
                while player_input != "confirm":
                    print(f"{str(Colors.RESET)} Où voulez-vous la placer > ")
                    player_input = input()

                    if player_input == "r":
                        self.board.restore()
                        piece.rotate()
                        # Preview
                        self.board.put(piece, x, y)

                        self.screen_clear()
                        self.board.display()
                        continue

                    if player_input[0] == "m":
                        self.board.restore()
                        piece.mirror(player_input[1] == "h", player_input[1] == "v")
                        # Preview
                        self.board.put(piece, x, y)
                        
                        self.screen_clear()
                        self.board.display()
                        continue

                    have_coord = player_input.split(",")
                    if len(have_coord) <= 1 or len(have_coord) > 2:
                        print("Coord invalid")
                        continue

                    x, y = have_coord
                    try:
                        x = int(x)
                        y = int(y)

                        self.board.restore()
                        # Preview
                        self.board.put(piece, x, y)
                    except ValueError:
                        print("Invalid number")
                        continue
                    except Exception as e:
                        print(e)
                        continue

                    self.screen_clear()
                    self.board.display()
                try:
                    player.place_piece(self.board, piece, x, y)
                except PieceNotInCornerException:
                    print("Au début du jeu, vous devez mettre votre piece dans un coin de la table")
                    self.board.restore()
                    continue
                except PieceOverlapException:
                    print("Votre piece recouvre une autre piece déjà posé sur la table")
                    self.board.restore()
                    continue
                except NotAdjacentPieceException:
                    print("Votre piece n'est pas dans un coin d'une autre piece")
                    self.board.restore()
                    continue
                except Exception as e:
                    print(e)
                    continue
                i += 1
            self.screen_clear()
            self.board.display()
            time.sleep(0.25)


game = Game(Board(20, 20))
game.screen_clear()
game.run()
