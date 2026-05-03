import copy
from moves import is_valid_move, make_move
 
# Board representation:
# 'A' = Attacker
# 'D' = Defender
# 'K' = King
# '.' = Empty

BOARD_SIZE = 9


def find_king(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 'K':
                return (i, j)
    return None


def count_pieces(board, piece):
    return sum(row.count(piece) for row in board)


def is_corner(pos):
    return pos in [(0, 0), (0, 8), (8, 0), (8, 8)]


def is_terminal(board):
    king_pos = find_king(board)

    # King reached corner → defenders win
    if is_corner(king_pos):
        return True

    # King captured → attackers win
    if is_king_surrounded(board):
        return True

    return False

# Movement

def get_all_moves(board, player):
    moves = []
    # Map M3's player string to M1/M2's turn string
    turn = 'A' if player == 'A' else 'D'

    for r1 in range(BOARD_SIZE):
        for c1 in range(BOARD_SIZE):
            piece = board[r1][c1]
            
            if (player == 'D' and piece in ['D', 'K']) or (player == 'A' and piece == 'A'):
                
                for c2 in range(BOARD_SIZE):
                    if is_valid_move(board, r1, c1, r1, c2, turn):
                        moves.append(((r1, c1), (r1, c2)))
                        
                for r2 in range(BOARD_SIZE):
                    if is_valid_move(board, r1, c1, r2, c1, turn):
                        moves.append(((r1, c1), (r2, c1)))

    return moves


def apply_move(board, move):
    new_board = copy.deepcopy(board)
    (r1, c1), (r2, c2) = move
    
    make_move(new_board, r1, c1, r2, c2)
    return new_board

# King Checks
 

def get_king_moves(board):
    king_pos = find_king(board)
    if not king_pos:
        return []

    r1, c1 = king_pos
    moves = []

    # Check horizontal moves
    for c2 in range(BOARD_SIZE):
        if is_valid_move(board, r1, c1, r1, c2, 'D'):
            moves.append(((r1, c1), (r1, c2)))

    # Check vertical moves
    for r2 in range(BOARD_SIZE):
        if is_valid_move(board, r1, c1, r2, c1, 'D'):
            moves.append(((r1, c1), (r2, c1)))

    return moves


def is_king_surrounded(board):
    x, y = find_king(board)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    count = 0

    for dx, dy in directions:
        nx, ny = x+dx, y+dy

        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[nx][ny] == 'A':
                count += 1

    return count >= 4


def attackers_near_king(board):
    x, y = find_king(board)
    count = 0

    for i in range(max(0, x-1), min(BOARD_SIZE, x+2)):
        for j in range(max(0, y-1), min(BOARD_SIZE, y+2)):
            if board[i][j] == 'A':
                count += 1

    return count


def king_on_edge(board):
    x, y = find_king(board)
    return x == 0 or x == 8 or y == 0 or y == 8


 
# Utility Function
 

def evaluate(board):
    score = 0

    king_pos = find_king(board)

    # Distance to corner
    corners = [(0,0),(0,8),(8,0),(8,8)]
    min_dist = min(abs(king_pos[0]-c[0]) + abs(king_pos[1]-c[1]) for c in corners)
    score += (20 - min_dist * 2)

    #  Pieces
    defenders = count_pieces(board, 'D')
    attackers = count_pieces(board, 'A')

    score += defenders * 3
    score -= attackers * 2

    #  King mobility
    score += len(get_king_moves(board)) * 5

    #  King danger
    if is_king_surrounded(board):
        score -= 100

    #  Extra tuning
    if king_on_edge(board):
        score += 10

    score -= attackers_near_king(board) * 5

    return score


 
#  Alpha-Beta
 

def alpha_beta(board, depth, alpha, beta, maximizing_player):

    if depth == 0 or is_terminal(board):
        return evaluate(board), None

    best_move = None

    if maximizing_player:  # Defender
        max_eval = float('-inf')

        for move in get_all_moves(board, 'D'):
            new_board = apply_move(board, move)
            eval_score, _ = alpha_beta(new_board, depth-1, alpha, beta, False)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move

    else:  # Attacker
        min_eval = float('inf')

        for move in get_all_moves(board, 'A'):
            new_board = apply_move(board, move)
            eval_score, _ = alpha_beta(new_board, depth-1, alpha, beta, True)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move


 
# Difficulty  
 

def get_ai_move(board, turn, difficulty="medium"):

    if difficulty == "easy":
        depth = 1
    elif difficulty == "medium":
        depth = 3
    elif difficulty == "hard":
        depth = 5
    else:
        depth = 3

    is_maximizing = (turn == 'D')

    _, move = alpha_beta(board, depth, float('-inf'), float('inf'), is_maximizing)
    return move


 
# Example Run
 

if __name__ == "__main__":
    # simple empty board with king center
    board = [['.' for _ in range(9)] for _ in range(9)]

    board[4][4] = 'K'

    # add some pieces
    board[4][3] = 'D'
    board[4][5] = 'D'
    board[3][4] = 'D'
    board[5][4] = 'D'

    board[0][4] = 'A'
    board[8][4] = 'A'
    board[4][0] = 'A'
    board[4][8] = 'A'

    move = get_ai_move(board, "medium")
    print("AI Move:", move)