SIZE = 9
EMPTY = "."
ATTACKER = "A"
DEFENDER = "D"
KING = "K"

THRONE = (4, 4)
CORNERS = [(0, 0), (0, 8), (8, 0), (8, 8)]


def create_board():
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

    # King
    board[4][4] = KING

    # Defenders
    defenders = [
        (4,3),(4,5),(3,4),(5,4),
        (4,2),(4,6),(2,4),(6,4),
        (3,3),(3,5),(5,3),(5,5)
    ]

    for r,c in defenders:
        board[r][c] = DEFENDER

    # Attackers
    attackers = [
        (0,3),(0,4),(0,5),
        (1,4),

        (8,3),(8,4),(8,5),
        (7,4),

        (3,0),(4,0),(5,0),
        (4,1),

        (3,8),(4,8),(5,8),
        (4,7)
    ]

    for r,c in attackers:
        board[r][c] = ATTACKER

    return board


def print_board(board):
    print("   0 1 2 3 4 5 6 7 8")
    for i,row in enumerate(board):
        print(i," ".join(row))