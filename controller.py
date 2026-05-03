
from board import print_board, ATTACKER, DEFENDER
from moves import is_valid_move, make_move
from capture import capture_after_move, king_escaped, king_captured
from AI import get_ai_move

def switch_turn(state):
    if state.turn == ATTACKER:
        state.turn = DEFENDER
    else:
        state.turn = ATTACKER


def play_game(state):
    print("--- HNEFATAFL ---")
    human_choice = input("Do you want to play Attackers (A) or Defenders (D)? ").strip().upper()
    human_side = ATTACKER if human_choice == 'A' else DEFENDER
    ai_side = DEFENDER if human_side == ATTACKER else ATTACKER
    
    difficulty = input("Select AI difficulty (easy, medium, hard): ").strip().lower()

    while state.winner is None:
        print_board(state.board)
        print()

        if state.turn == ai_side:
            print(f"Computer ({ai_side}) is thinking...")
            
            ai_move = get_ai_move(state.board,state.turn, difficulty)
            
            if ai_move:
                (r1, c1), (r2, c2) = ai_move
                make_move(state.board, r1, c1, r2, c2)
                capture_after_move(state.board, r2, c2, state.turn)
                print(f"Computer moved from ({r1}, {c1}) to ({r2}, {c2})")
            else:
                print("Computer has no valid moves!")
                state.winner = "Human"
                break
                
        else:
            print("Your Turn")
            try:
                r1 = int(input("From row: "))
                c1 = int(input("From col: "))
                r2 = int(input("To row: "))
                c2 = int(input("To col: "))
            except ValueError:
                print("Invalid input! Please enter numbers.")
                continue

            if not is_valid_move(state.board, r1, c1, r2, c2, state.turn):
                print("Invalid move. Try again.")
                continue

            make_move(state.board, r1, c1, r2, c2)
            capture_after_move(state.board, r2, c2, state.turn)

        if king_escaped(state.board):
            state.winner = "Defenders"
        elif king_captured(state.board):
            state.winner = "Attackers"
        else:
            switch_turn(state)

    print_board(state.board)
    print(f"\nGame Over! Winner: {state.winner}")