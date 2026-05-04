import pygame
import sys
from board import create_board, ATTACKER, DEFENDER, KING
from state import GameState
from moves import is_valid_move, make_move, piece_belongs
from capture import capture_after_move, king_escaped, king_captured
from AI import get_ai_move

# --- CONSTANTS ---
WIDTH, HEIGHT = 720, 720
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS

# --- BOARD COLORS (RGB) ---
LIGHT_WOOD = (240, 217, 181)
DARK_WOOD = (181, 136, 99)
THRONE_COLOR = (200, 150, 100)
CORNER_COLOR = (150, 100, 50)

# --- PIECE COLORS (RGB) ---
ATTACKER_COLOR = (50, 50, 50)    # Dark Grey/Black
DEFENDER_COLOR = (220, 220, 220) # Off-White/Light Grey
KING_COLOR = (255, 215, 0)       # Gold
HIGHLIGHT_COLOR = (50, 205, 50)  # Nice visible Green

def draw_grid(window):
    """Draws the alternating square colors and special Hnefatafl tiles."""
    window.fill(LIGHT_WOOD)
    
    for row in range(ROWS):
        for col in range(COLS):
            # Standard alternating checkerboard pattern
            if (row + col) % 2 == 1:
                pygame.draw.rect(window, DARK_WOOD, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight the Throne (Center)
            if row == 4 and col == 4:
                pygame.draw.rect(window, THRONE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
            # Highlight the 4 Corners
            if (row, col) in [(0, 0), (0, 8), (8, 0), (8, 8)]:
                pygame.draw.rect(window, CORNER_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_highlight(window, row, col):
    """Draws a green outline around the selected square."""
    pygame.draw.rect(window, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def draw_pieces(window, board):
    """Draws the pieces on the board based on the backend state."""
    # We want the pieces to be slightly smaller than the square
    radius = SQUARE_SIZE // 2 - 10 

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            
            if piece != '.':
                # Calculate the center (x, y) of the square
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

                if piece == ATTACKER:
                    pygame.draw.circle(window, ATTACKER_COLOR, (center_x, center_y), radius)
                    # Optional: Draw an outline to make it look nicer
                    pygame.draw.circle(window, (0,0,0), (center_x, center_y), radius, 2)
                    
                elif piece == DEFENDER:
                    pygame.draw.circle(window, DEFENDER_COLOR, (center_x, center_y), radius)
                    pygame.draw.circle(window, (0,0,0), (center_x, center_y), radius, 2)
                    
                elif piece == KING:
                    pygame.draw.circle(window, KING_COLOR, (center_x, center_y), radius)
                    pygame.draw.circle(window, (0,0,0), (center_x, center_y), radius, 2)

def start_menu(window):
    """Displays a pre-game menu to choose side and difficulty."""
    font = pygame.font.SysFont('Arial', 60, bold=True)
    small_font = pygame.font.SysFont('Arial', 30)
    
    difficulty = "medium" # Default
    
    while True:
        window.fill(LIGHT_WOOD)
        
        # Draw Title
        title = font.render("HNEFATAFL", True, (0, 0, 0))
        window.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw Difficulty Status
        diff_text = small_font.render(f"Difficulty: {difficulty.upper()} (Press 1=Easy, 2=Med, 3=Hard)", True, (100, 100, 100))
        window.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 250))
        
        # Draw Side Selection Instructions
        inst1 = small_font.render("Press 'A' to play Attackers (You move first)", True, (0, 0, 0))
        inst2 = small_font.render("Press 'D' to play Defenders (AI moves first)", True, (0, 0, 0))
        
        window.blit(inst1, (WIDTH//2 - inst1.get_width()//2, 400))
        window.blit(inst2, (WIDTH//2 - inst2.get_width()//2, 480))
        
        pygame.display.update()
        
        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Change difficulty
                if event.key == pygame.K_1: difficulty = "easy"
                if event.key == pygame.K_2: difficulty = "medium"
                if event.key == pygame.K_3: difficulty = "hard"
                
                # Choose side and start game
                if event.key == pygame.K_a:
                    return ATTACKER, DEFENDER, difficulty
                if event.key == pygame.K_d:
                    return DEFENDER, ATTACKER, difficulty


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hnefatafl - AI Project")
    clock = pygame.time.Clock()

    # --- CALL THE START MENU ---
    human_side, ai_side, difficulty = start_menu(window)
    
    # --- INITIALIZE BOARD ---
    board_data = create_board()
    state = GameState(board_data)
    selected_square = None 

    running = True
    while running:
        clock.tick(60)
        
        # --- 1. AI TURN LOGIC ---
        if state.turn == ai_side and state.winner is None:
            # Force the screen to update so the user sees their last move before AI thinks
            draw_grid(window)
            draw_pieces(window, state.board)
            pygame.display.update()
            
            print(f"Computer ({ai_side}) is thinking...")
            ai_move = get_ai_move(state.board, state.turn, difficulty)
            
            if ai_move:
                (r1, c1), (r2, c2) = ai_move
                make_move(state.board, r1, c1, r2, c2)
                capture_after_move(state.board, r2, c2, state.turn)
                print(f"Computer moved from ({r1}, {c1}) to ({r2}, {c2})")
            else:
                state.winner = "Human" # AI got stuck

            # Check for win conditions
            if king_escaped(state.board): state.winner = "Defenders"
            elif king_captured(state.board): state.winner = "Attackers"
            else:
                state.turn = human_side # Switch back to human

        # --- 2. HUMAN TURN & EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            # Handle Mouse Clicks only if it's the Human's turn and game isn't over
            if event.type == pygame.MOUSEBUTTONDOWN and state.winner is None and state.turn == human_side:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                
                # If we ALREADY have a piece selected, try to move it
                if selected_square:
                    r1, c1 = selected_square
                    r2, c2 = row, col
                    
                    # If clicking the exact same square, deselect it
                    if selected_square == (r2, c2):
                        selected_square = None
                        
                    # If clicking a valid destination
                    elif is_valid_move(state.board, r1, c1, r2, c2, state.turn):
                        make_move(state.board, r1, c1, r2, c2)
                        capture_after_move(state.board, r2, c2, state.turn)
                        
                        # Check win conditions
                        if king_escaped(state.board): state.winner = "Defenders"
                        elif king_captured(state.board): state.winner = "Attackers"
                        else:
                            state.turn = ai_side # Give turn to computer
                            
                        selected_square = None # Reset selection
                        
                    # If invalid move, just deselect (or play an error sound!)
                    else:
                        print("Invalid move")
                        selected_square = None
                        
                # If NO piece is selected, try to select one
                else:
                    piece = state.board[row][col]
                    if piece != '.' and piece_belongs(piece, state.turn):
                        selected_square = (row, col)

        # --- 3. RENDERING ---
        draw_grid(window)
        
        # Draw the green highlight box if a piece is selected
        if selected_square:
            draw_highlight(window, selected_square[0], selected_square[1])
            
        draw_pieces(window, state.board)
        
        # --- 4. GAME OVER OVERLAY ---
        if state.winner:
            font = pygame.font.SysFont('Arial', 80, bold=True)
            text = font.render(f"{state.winner} Win!", True, (255, 0, 0)) # Red text
            
            # Center the text on screen
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            # Draw a dark background box behind text so it's readable
            bg_rect = pygame.Rect(text_rect.left - 20, text_rect.top - 20, text_rect.width + 40, text_rect.height + 40)
            pygame.draw.rect(window, (0, 0, 0), bg_rect)
            window.blit(text, text_rect)

        pygame.display.update()

if __name__ == "__main__":
    main()
