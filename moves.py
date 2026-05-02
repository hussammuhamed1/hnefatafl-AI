from board import EMPTY, ATTACKER, DEFENDER, KING
from utils import inside


def piece_belongs(piece, turn):
    if turn == ATTACKER:
        return piece == ATTACKER
    else:
        return piece == DEFENDER or piece == KING


def is_valid_move(board, r1,c1,r2,c2, turn):

    if not inside(r1,c1) or not inside(r2,c2):
        return False

    piece = board[r1][c1]

    if piece == EMPTY:
        return False

    if not piece_belongs(piece, turn):
        return False

    if board[r2][c2] != EMPTY:
        return False

    if r1 != r2 and c1 != c2:
        return False

    # path clear
    if r1 == r2:
        step = 1 if c2 > c1 else -1
        for c in range(c1 + step, c2, step):
            if board[r1][c] != EMPTY:
                return False

    if c1 == c2:
        step = 1 if r2 > r1 else -1
        for r in range(r1 + step, r2, step):
            if board[r][c1] != EMPTY:
                return False

    return True


def make_move(board, r1,c1,r2,c2):
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = EMPTY