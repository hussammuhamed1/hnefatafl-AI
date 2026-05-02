
from board import print_board, ATTACKER, DEFENDER
from moves import is_valid_move, make_move
from capture import capture_after_move, king_escaped, king_captured


def switch_turn(state):
    if state.turn == ATTACKER:
        state.turn = DEFENDER
    else:
        state.turn = ATTACKER


def play_game(state):

    while state.winner is None:

        print_board(state.board)
        print()

        if state.turn == ATTACKER:
            print("Attackers Turn")
        else:
            print("Defenders Turn")

        try:
            r1 = int(input("From row: "))
            c1 = int(input("From col: "))
            r2 = int(input("To row: "))
            c2 = int(input("To col: "))

        except:
            print("Invalid input")
            continue

        if not is_valid_move(state.board, r1,c1,r2,c2,state.turn):
            print("Invalid move")
            continue

        make_move(state.board, r1,c1,r2,c2)

        capture_after_move(state.board, r2,c2,state.turn)

        if king_escaped(state.board):
            state.winner = "Defenders"

        elif king_captured(state.board):
            state.winner = "Attackers"

        else:
            switch_turn(state)

    print_board(state.board)
    print()
    print("Winner:", state.winner)