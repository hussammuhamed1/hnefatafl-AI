class GameState:
    def __init__(self, board):
        self.board = board
        self.turn = "A"   
        self.winner = None