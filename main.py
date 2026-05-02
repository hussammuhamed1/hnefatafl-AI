from board import create_board
from state import GameState
from controller import play_game

board = create_board()
state = GameState(board)

play_game(state)