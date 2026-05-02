from board import EMPTY, ATTACKER, DEFENDER, KING, CORNERS, THRONE
from utils import inside


def enemy(piece, turn):
    if turn == ATTACKER:
        return piece == DEFENDER
    else:
        return piece == ATTACKER


def ally(piece, turn):
    if turn == ATTACKER:
        return piece == ATTACKER
    else:
        return piece == DEFENDER or piece == KING


def capture_after_move(board, r, c, turn):

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr,dc in directions:

        r1 = r + dr
        c1 = c + dc

        r2 = r + dr*2
        c2 = c + dc*2

        if not inside(r1,c1):
            continue

        target = board[r1][c1]

        if target == EMPTY or target == KING:
            continue

        if enemy(target, turn):

            hostile = False

            if inside(r2,c2):
                if ally(board[r2][c2], turn):
                    hostile = True
                if (r2,c2) in CORNERS or (r2,c2) == THRONE:
                    hostile = True
            else:
                hostile = False

            if hostile:
                board[r1][c1] = EMPTY


def king_position(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == KING:
                return (r,c)
    return None


def king_escaped(board):
    pos = king_position(board)
    return pos in CORNERS


def king_captured(board):
    pos = king_position(board)

    if pos is None:
        return True

    r,c = pos

    count = 0
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr,dc in dirs:
        nr = r + dr
        nc = c + dc

        if not inside(nr,nc):
            count += 1
        elif board[nr][nc] == ATTACKER:
            count += 1


    if r == 0 or r == 8 or c == 0 or c == 8:
        return count >= 3

    return count == 4