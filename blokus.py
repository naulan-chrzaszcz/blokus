"""Blockus

This script runs a blokus game with customizable options.

Arguments:
    - <nb_players>: (int) Number of players. Default is 4.
    - <width>x<height>: (str) Dimensions of the board in the format <int>x<int>. Example: 20x20. Default is 20x20.
"""
import random
import sys
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
    
    nb_players: int
    players: List[Player]
    pieces: List[Piece]
    board: Board

    def __init__(self, board: Board = Board(20, 20), nb_players: int = 4) -> None:
        """Create a new instance of the Game.

        Args:
            board (Board): The game board on which the game is played.
        """
        self.board = board
        
        self.nb_players = nb_players
        self.players = []
        self.pieces = []
        self.__load_ressources()

        # Create and attribute color to player
        colors = self.PLAYERS_COLOR.copy()
        for _ in range(self.nb_players):
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
        i = 0
        while True:
            player = self.players[i%self.nb_players]

            self.screen_clear()
            print(f"Nombre de tours: {i}")
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
            print(f"Nombre de tours: {i}")
            self.board.display()

            player_input = ""
            self.board.save()
            while player_input != "confirm":
                self.screen_clear()
                print(f"Nombre de tours: {i}")
                self.board.display()
                
                print(f"{str(Colors.RESET)} Où voulez-vous la placer > ")
                player_input = input()

                if player_input == "confirm":
                    continue

                if player_input == "r":
                    self.board.restore()
                    piece.rotate()
                    # Preview
                    self.board.put(piece, x, y)
                    continue

                if player_input[0] == "m":
                    self.board.restore()
                    piece.mirror(player_input[1] == "h", player_input[1] == "v")
                    # Preview
                    self.board.put(piece, x, y)
                    continue

                have_coord = player_input.split(",")
                if len(have_coord) <= 1 or len(have_coord) > 2:
                    print(f"{str(Colors.RED)}Emplacement invalide !{str(Colors.RESET)}")
                    continue

                x, y = have_coord
                try:
                    x = int(x)
                    y = int(y)

                    self.board.restore()
                    # Preview
                    self.board.put(piece, x, y)
                except ValueError:
                    print(f"{str(Colors.RED)}Les valeurs entrée ne sont pas des nombres !{str(Colors.RESET)}")
                    continue
                except Exception as e:
                    print(e)
                    continue

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


launch_args = sys.argv
if len(launch_args) > 1:
    nb_players = -1
    width = -1
    height = -1

    # Argument 1: Number of players (required)
    try:
        nb_players = int(launch_args[1])
    except ValueError:
        print(f"{str(Colors.RED)}Le nombre de joueur doit être un nombre !{str(Colors.RESET)}")
        exit(-1)
    except Exception as e:
        print(e)
        exit(-1)
    
    if nb_players < 2 or nb_players > 4:
        print(f"{str(Colors.RED)}Il y a pas assez ou trop de joueur !{str(Colors.RESET)}")
        exit(-1)

    # Argument 2: Board dimensions (optional, in the format <width>x<height>)
    try:
        board_dimension = launch_args[2].split('x')
        width = int(board_dimension[0])
        height = int(board_dimension[1])
    except IndexError:
        print(f"{str(Colors.RED)}La specification de la taille du tableau est incorrect, veuillez suivre comme suis : <int>x<int>{str(Colors.RESET)}")
    except ValueError:
        print(f"{str(Colors.RED)}Les valeurs specifié pour la taille du tableau n'est pas des nombres decimal !{str(Colors.RESET)}")
    except Exception as e:
        print(e)
        exit(-1)

    board: Board = None
    if width > -1 and height > -1:
        board = Board(width, height)
    
    game = Game(nb_players=nb_players)
    if board is not None:
        game = Game(board, nb_players)
        game.run()
        exit()
    game.run()
    exit()

game = Game()
game.run()
