import pygame
import sys
import random
import time
 
# Initialize Pygame
pygame.init()
 
# Constants
WINDOW_SIZE = 680
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0, 128)
VALID_MOVE = (0, 255, 0, 128)
FPS = 144  # Increased FPS for smoother gameplay
 
# Colors for the board
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
 
# Add these colors to the constants section at the top
SELECTED_PIECE = (255, 255, 0, 180)  # Brighter yellow for selected piece
VALID_MOVE_HIGHLIGHT = (124, 252, 0, 160)  # Bright green for valid moves
LAST_MOVE = (135, 206, 250, 160)  # Light blue for showing last move
CHECKED_KING = (255, 0, 0, 180)  # Red highlight for checked king
 
# Menu settings
MENU_BG = (25, 25, 35)  # Darker background
MENU_TITLE_COLOR = (255, 255, 255)  # White text
MENU_BUTTON_BG = (45, 45, 55)  # Slightly lighter than background
MENU_BUTTON_HOVER = (65, 65, 75)  # Hover color
MENU_BUTTON_SELECTED = (85, 85, 95)  # Selected color
MENU_TEXT_COLOR = (255, 255, 255)  # White text for buttons
MENU_ACCENT_COLOR = (0, 150, 255)  # Blue accent color
MENU_BORDER_COLOR = (100, 100, 110)  # Border color
MENU_MARGIN = 40  # Margin from screen edges
MENU_PADDING = 20  # Padding between elements
 
# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game with AI")
 
# Chess piece Unicode characters
PIECES = {
    'white': {
        'king': '♔',
        'queen': '♕',
        'rook': '♖',
        'bishop': '♗',
        'knight': '♘',
        'pawn': '♙'
    },
    'black': {
        'king': '♚',
        'queen': '♛',
        'rook': '♜',
        'bishop': '♝',
        'knight': '♞',
        'pawn': '♟'
    }
}
 
# Piece values for evaluation
PIECE_VALUES = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000
}
 
# Menu settings
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.selected = False
        self.hover = False
        self.animation_offset = 0
        self.animation_speed = 0.2
        self.target_offset = 0
 
    def draw(self, surface):
        # Animate button position
        if self.animation_offset != self.target_offset:
            self.animation_offset += (self.target_offset - self.animation_offset) * self.animation_speed
       
        # Create animated rect
        animated_rect = self.rect.copy()
        animated_rect.y += self.animation_offset
       
        # Draw button with hover effect
        if self.hover:
            pygame.draw.rect(surface, MENU_BUTTON_HOVER, animated_rect)
            # Draw glow effect
            glow_surface = pygame.Surface((animated_rect.width + 20, animated_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*MENU_ACCENT_COLOR, 30), (10, 10, animated_rect.width, animated_rect.height), border_radius=10)
            surface.blit(glow_surface, (animated_rect.x - 10, animated_rect.y - 10))
        elif self.selected:
            pygame.draw.rect(surface, MENU_BUTTON_SELECTED, animated_rect)
        else:
            pygame.draw.rect(surface, self.color, animated_rect)
       
        # Draw border with gradient effect
        border_color = MENU_ACCENT_COLOR if self.hover or self.selected else MENU_BORDER_COLOR
        pygame.draw.rect(surface, border_color, animated_rect, 2)
       
        # Draw text with shadow
        font = pygame.font.SysFont('Arial', 32, bold=True)
        # Shadow
        shadow = font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(animated_rect.centerx + 2, animated_rect.centery + 2))
        surface.blit(shadow, shadow_rect)
        # Main text
        text_surface = font.render(self.text, True, MENU_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=animated_rect.center)
        surface.blit(text_surface, text_rect)
 
def draw_menu():
    screen.fill(MENU_BG)
   
    # Draw background pattern with margin
    for i in range(MENU_MARGIN, WINDOW_SIZE - MENU_MARGIN, 40):
        pygame.draw.line(screen, (35, 35, 45), (i, MENU_MARGIN), (i, WINDOW_SIZE - MENU_MARGIN))
    for i in range(MENU_MARGIN, WINDOW_SIZE - MENU_MARGIN, 40):
        pygame.draw.line(screen, (35, 35, 45), (MENU_MARGIN, i), (WINDOW_SIZE - MENU_MARGIN, i))
   
    # Draw title with enhanced shadow effect and proper margin
    font_title = pygame.font.SysFont('Arial', 72, bold=True)
    # Multiple shadow layers for depth
    for offset in range(3, 0, -1):
        shadow = font_title.render("Chess Game", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(WINDOW_SIZE // 2 + offset, MENU_MARGIN + 102 + offset))
        screen.blit(shadow, shadow_rect)
    # Main text with gradient effect
    title = font_title.render("Chess Game", True, MENU_TITLE_COLOR)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, MENU_MARGIN + 100))
    screen.blit(title, title_rect)
   
    # Create buttons with new styling and proper spacing
    button_width = 300
    button_height = 80
    button_spacing = 40  # Increased spacing between buttons
   
    # Calculate vertical positions for better spacing
    total_height = button_height * 2 + button_spacing  # Height of mode buttons
    start_y = (WINDOW_SIZE - total_height) // 2  # Center the buttons vertically
   
    # Create mode selection buttons
    player_button = Button(WINDOW_SIZE//2 - button_width//2, start_y, button_width, button_height, "Play with Friend", MENU_BUTTON_BG)
    ai_button = Button(WINDOW_SIZE//2 - button_width//2, start_y + button_height + button_spacing, button_width, button_height, "Play with AI", MENU_BUTTON_BG)
   
    # Create start button (will be positioned in menu_loop)
    start_button = Button(WINDOW_SIZE//2 - 150, 0, 300, 60, "Start Game", MENU_BUTTON_BG)  # Width increased for better proportion
   
    return player_button, ai_button, start_button
 
def menu_loop():
    player_button, ai_button, start_button = draw_menu()
    game_mode = None
    clock = pygame.time.Clock()
   
    # Initialize button states
    player_button.selected = False
    ai_button.selected = False
    start_button.selected = False
   
    # Animation states
    buttons = [player_button, ai_button, start_button]
    for i, button in enumerate(buttons):
        button.target_offset = 50
        button.animation_offset = 50
   
    while True:
        # Clear screen
        screen.fill(MENU_BG)
       
        # Draw background pattern with margin
        for i in range(MENU_MARGIN, WINDOW_SIZE - MENU_MARGIN, 40):
            pygame.draw.line(screen, (35, 35, 45), (i, MENU_MARGIN), (i, WINDOW_SIZE - MENU_MARGIN))
        for i in range(MENU_MARGIN, WINDOW_SIZE - MENU_MARGIN, 40):
            pygame.draw.line(screen, (35, 35, 45), (MENU_MARGIN, i), (WINDOW_SIZE - MENU_MARGIN, i))
       
        # Draw title with enhanced shadow effect
        font_title = pygame.font.SysFont('Arial', 72, bold=True)
        # Multiple shadow layers for depth
        for offset in range(3, 0, -1):
            shadow = font_title.render("Chess Game", True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(WINDOW_SIZE // 2 + offset, MENU_MARGIN + 102 + offset))
            screen.blit(shadow, shadow_rect)
        # Main text
        title = font_title.render("Chess Game", True, MENU_TITLE_COLOR)
        title_rect = title.get_rect(center=(WINDOW_SIZE // 2, MENU_MARGIN + 100))
        screen.blit(title, title_rect)
       
        # Draw buttons
        player_button.draw(screen)
        ai_button.draw(screen)
       
        # Only show start button and selection text if a mode is selected
        if game_mode:
            # Draw selection text with enhanced styling
            font = pygame.font.SysFont('Arial', 28, bold=True)
            mode_text = f"Selected: {'Player vs Player' if game_mode == 'player' else 'Player vs AI'}"
            text_surface = font.render(mode_text, True, MENU_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, ai_button.rect.bottom + 60))
           
            # Draw background panel for selection text with animation
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(40, 20)
           
            # Add hover effect to the selection text
            mouse_pos = pygame.mouse.get_pos()
            if bg_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, MENU_BUTTON_HOVER, bg_rect)
                pygame.draw.rect(screen, MENU_ACCENT_COLOR, bg_rect, 2)
            else:
                pygame.draw.rect(screen, MENU_BUTTON_BG, bg_rect)
                pygame.draw.rect(screen, MENU_BORDER_COLOR, bg_rect, 2)
           
            # Draw text with shadow
            shadow = font.render(mode_text, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
            screen.blit(shadow, shadow_rect)
            screen.blit(text_surface, text_rect)
           
            # Add interactive elements to the selection text
            if bg_rect.collidepoint(mouse_pos):
                # Draw a small arrow indicator
                arrow_points = [
                    (text_rect.right + 10, text_rect.centery),
                    (text_rect.right + 20, text_rect.centery - 5),
                    (text_rect.right + 20, text_rect.centery + 5)
                ]
                pygame.draw.polygon(screen, MENU_ACCENT_COLOR, arrow_points)
           
            # Position and draw start button below selection text
            start_button.rect.centerx = WINDOW_SIZE // 2
            start_button.rect.top = text_rect.bottom + 40
            start_button.draw(screen)
       
        pygame.display.flip()
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
               
                # Check button clicks with improved touch sensitivity
                if player_button.rect.collidepoint(mouse_pos):
                    game_mode = "player"
                    player_button.selected = True
                    ai_button.selected = False
                    # Animate buttons
                    player_button.target_offset = 0
                    ai_button.target_offset = 0
                   
                elif ai_button.rect.collidepoint(mouse_pos):
                    game_mode = "ai"
                    ai_button.selected = True
                    player_button.selected = False
                    # Animate buttons
                    player_button.target_offset = 0
                    ai_button.target_offset = 0
                   
                elif game_mode and start_button.rect.collidepoint(mouse_pos):
                    # Add click animation for start button
                    start_button.rect.y += 5
                    pygame.display.flip()
                    pygame.time.wait(100)
                    start_button.rect.y -= 5
                    return game_mode
           
            # Add hover effect for buttons with improved touch sensitivity
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Add a small hitbox extension for better touch sensitivity
                extended_rect = start_button.rect.copy()
                extended_rect.inflate_ip(20, 20)
                player_button.hover = player_button.rect.collidepoint(mouse_pos)
                ai_button.hover = ai_button.rect.collidepoint(mouse_pos)
                start_button.hover = extended_rect.collidepoint(mouse_pos) if game_mode else False
       
        clock.tick(FPS)
 
# Game logic functions
def get_raw_moves(board, start_pos, piece):
    """Get moves without considering check (to avoid recursion)"""
    valid_moves = []
    row, col = start_pos
    piece_type = piece[1]
    piece_color = piece[0]
    direction = 1 if piece_color == 'white' else -1
 
    if piece_type == 'pawn':
        # Forward move
        new_row = row + direction
        if 0 <= new_row < BOARD_SIZE:
            if not board[new_row][col]:
                valid_moves.append((new_row, col))
                if (piece_color == 'white' and row == 1) or (piece_color == 'black' and row == 6):
                    new_row = row + 2 * direction
                    if 0 <= new_row < BOARD_SIZE and not board[new_row][col]:
                        valid_moves.append((new_row, col))
       
        # Diagonal captures
        for dcol in [-1, 1]:
            new_col = col + dcol
            new_row = row + direction
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if target and target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    elif piece_type in ['rook', 'bishop', 'queen']:
        directions = []
        if piece_type in ['rook', 'queen']:
            directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
        if piece_type in ['bishop', 'queen']:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
           
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            while 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target:
                    valid_moves.append((new_row, new_col))
                else:
                    if target[0] != piece_color:
                        valid_moves.append((new_row, new_col))
                    break
                new_row += drow
                new_col += dcol
 
    elif piece_type == 'knight':
        moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        for new_row, new_col in moves:
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    elif piece_type == 'king':
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    return valid_moves
 
def get_valid_moves(board, start_pos, piece):
    valid_moves = []
    raw_moves = get_raw_moves(board, start_pos, piece)
   
    # Test each move to ensure it doesn't leave or put the king in check
    for move in raw_moves:
        temp_board = [row[:] for row in board]
        temp_board[move[0]][move[1]] = piece
        temp_board[start_pos[0]][start_pos[1]] = ''
       
        if not is_in_check(temp_board, piece[0]):
            valid_moves.append(move)
   
    return valid_moves
 
def evaluate_board(board):
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                value = PIECE_VALUES[piece[1]]
                if piece[0] == 'white':
                    score += value
                else:
                    score -= value
    return score
 
# Add performance monitoring
def show_fps(screen, clock):
    font = pygame.font.SysFont('Arial', 20)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'FPS: {fps}', True, BLACK)
    screen.blit(fps_text, (10, 10))
 
# Optimize minimax with move ordering and better pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(board), None
 
 
 # Pre-calculate all valid moves and sort them by potential value
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece and piece[0] == ('white' if maximizing_player else 'black'):
                valid_moves = get_valid_moves(board, (row, col), piece)
                for move in valid_moves:
                    # Quick evaluation of move
                    temp_board = [row[:] for row in board]
                    temp_board[move[0]][move[1]] = piece
                    temp_board[row][col] = ''
                    score = evaluate_board(temp_board)
                    moves.append((score, (row, col), move))
   
    # Sort moves by score
    moves.sort(reverse=maximizing_player)
 
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for _, start, end in moves:
            piece = board[start[0]][start[1]]
            temp_board = [row[:] for row in board]
            temp_board[end[0]][end[1]] = piece
            temp_board[start[0]][start[1]] = ''
           
            eval, _ = minimax(temp_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = (start, end)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for _, start, end in moves:
            piece = board[start[0]][start[1]]
            temp_board = [row[:] for row in board]
            temp_board[end[0]][end[1]] = piece
            temp_board[start[0]][start[1]] = ''
           
            eval, _ = minimax(temp_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = (start, end)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
 
def make_ai_move(board):
    _, best_move = minimax(board, 3, float('-inf'), float('inf'), False)
    if best_move:
        start_pos, end_pos = best_move
        piece = board[start_pos[0]][start_pos[1]]
        board[end_pos[0]][end_pos[1]] = piece
        board[start_pos[0]][start_pos[1]] = ''
        return True
    return False
 
def create_board():
    board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
   
    # Set up pawns
    for i in range(BOARD_SIZE):
        board[1][i] = ('white', 'pawn')
        board[6][i] = ('black', 'pawn')
   
    # Set up other pieces
    pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(BOARD_SIZE):
        board[0][i] = ('white', pieces[i])
        board[7][i] = ('black', pieces[i])
   
    return board
 
def draw_board(screen, selected_piece=None, valid_moves=None, last_move=None):
    # First draw the base board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
   
    # Draw last move highlight
    if last_move:
        start, end = last_move
        for pos in [start, end]:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(128)
            s.fill(LAST_MOVE)
            screen.blit(s, (pos[1] * SQUARE_SIZE, pos[0] * SQUARE_SIZE))
   
    # Draw valid moves with better visibility
    if valid_moves:
        for row, col in valid_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(160)
            s.fill(VALID_MOVE_HIGHLIGHT)
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # Draw a border around valid move squares
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
   
    # Draw selected piece highlight with better visibility
    if selected_piece:
        row, col = selected_piece
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(180)
        s.fill(SELECTED_PIECE)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        # Draw a border around selected piece
        pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
   
    # Draw pieces
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                color = WHITE if piece[0] == 'white' else BLACK
                font = pygame.font.SysFont('segoeuisymbol', SQUARE_SIZE // 2)
                text = font.render(PIECES[piece[0]][piece[1]], True, color)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text, text_rect)
               
                # Highlight king in red if in check
                if piece[1] == 'king' and is_in_check(board, piece[0]):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(180)
                    s.fill(CHECKED_KING)
                    screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    pygame.draw.rect(screen, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
 
def get_board_position(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
 
def is_valid_move(start, end, piece):
    valid_moves = get_valid_moves(board, start, piece)
    return end in valid_moves
 
def is_in_check(board, color):
    # Find king position
    king_pos = None
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece and piece[0] == color and piece[1] == 'king':
                king_pos = (row, col)
                break
        if king_pos:
            break
   
    # Check if any opponent piece can attack the king
    opponent = 'black' if color == 'white' else 'white'
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece and piece[0] == opponent:
                moves = get_raw_moves(board, (row, col), piece)  # Use raw moves to avoid recursion
                if king_pos in moves:
                    return True
    return False
 
def is_checkmate(board, color):
    if not is_in_check(board, color):
        return False
   
    # Try all possible moves for all pieces
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece and piece[0] == color:
                valid_moves = get_valid_moves(board, (row, col), piece)
                for move in valid_moves:
                    # Try the move
                    temp_board = [row[:] for row in board]
                    temp_board[move[0]][move[1]] = piece
                    temp_board[row][col] = ''
                   
                    # If this move gets us out of check, it's not checkmate
                    if not is_in_check(temp_board, color):
                        return False
    return True
 
def is_stalemate(board, color):
    if is_in_check(board, color):
        return False
   
    # Check if any piece has valid moves
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece and piece[0] == color:
                valid_moves = get_valid_moves(board, (row, col), piece)
                if valid_moves:
                    return False
    return True
 
def get_raw_moves(board, start_pos, piece):
    """Get moves without considering check (to avoid recursion)"""
    valid_moves = []
    row, col = start_pos
    piece_type = piece[1]
    piece_color = piece[0]
    direction = 1 if piece_color == 'white' else -1
 
    if piece_type == 'pawn':
        # Forward move
        new_row = row + direction
        if 0 <= new_row < BOARD_SIZE:
            if not board[new_row][col]:
                valid_moves.append((new_row, col))
                if (piece_color == 'white' and row == 1) or (piece_color == 'black' and row == 6):
                    new_row = row + 2 * direction
                    if 0 <= new_row < BOARD_SIZE and not board[new_row][col]:
                        valid_moves.append((new_row, col))
       
        # Diagonal captures
        for dcol in [-1, 1]:
            new_col = col + dcol
            new_row = row + direction
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if target and target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    elif piece_type in ['rook', 'bishop', 'queen']:
        directions = []
        if piece_type in ['rook', 'queen']:
            directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
        if piece_type in ['bishop', 'queen']:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
           
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            while 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target:
                    valid_moves.append((new_row, new_col))
                else:
                    if target[0] != piece_color:
                        valid_moves.append((new_row, new_col))
                    break
                new_row += drow
                new_col += dcol
 
    elif piece_type == 'knight':
        moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        for new_row, new_col in moves:
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    elif piece_type == 'king':
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board[new_row][new_col]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_row, new_col))
 
    return valid_moves
 
# Modify the game loop to handle check and checkmate
def draw_game_status(screen, current_player, is_check, is_mate):
    font = pygame.font.SysFont('Arial', 32)  # Increased font size
    status_text = ""
    text_color = BLACK
   
    if is_mate:
        winner = 'Black' if current_player == 'white' else 'White'
        status_text = f"Checkmate! {winner} wins!"
    elif is_check:
        status_text = f"{current_player.capitalize()} is in CHECK!"
        text_color = (255, 0, 0)  # Red color for check warning
   
    if status_text:
        text_surface = font.render(status_text, True, text_color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, 30))
        # Draw background for text with padding
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(40, 20)  # Increased padding
        pygame.draw.rect(screen, WHITE, bg_rect)
        if is_check:
            pygame.draw.rect(screen, (255, 0, 0), bg_rect, 2)  # Red border for check
        else:
            pygame.draw.rect(screen, BLACK, bg_rect, 1)
        screen.blit(text_surface, text_rect)
 
# Initialize the game
board = create_board()
selected_piece = None
current_player = 'white'
valid_moves = None
ai_thinking = False
 
# Menu loop to choose game mode
game_mode = menu_loop()
 
# Optimize the game loop
running = True
clock = pygame.time.Clock()
 
# Add last_move tracking to store the last move made
last_move = None
 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:  # Restart game
                board = create_board()
                selected_piece = None
                current_player = 'white'
                valid_moves = None
                ai_thinking = False
                last_move = None
        elif event.type == pygame.MOUSEBUTTONDOWN and not ai_thinking:
            pos = get_board_position(event.pos)
            if event.button == 1:  # Left click
                if selected_piece is None:
                    piece = board[pos[0]][pos[1]]
                    if piece and piece[0] == current_player:
                        selected_piece = pos
                        valid_moves = get_valid_moves(board, pos, piece)
                else:
                    piece = board[selected_piece[0]][selected_piece[1]]
                    # Check if clicking on the same piece
                    if pos == selected_piece:
                        selected_piece = None
                        valid_moves = None
                    # Check if clicking on a valid move
                    elif is_valid_move(selected_piece, pos, piece):
                        # Make the move
                        board[pos[0]][pos[1]] = piece
                        board[selected_piece[0]][selected_piece[1]] = ''
                        # Store last move
                        last_move = (selected_piece, pos)
                        # Switch player
                        current_player = 'black' if current_player == 'white' else 'white'
                        selected_piece = None
                        valid_moves = None
                    # Click on different piece of same color
                    elif board[pos[0]][pos[1]] and board[pos[0]][pos[1]][0] == current_player:
                        selected_piece = pos
                        valid_moves = get_valid_moves(board, pos, board[pos[0]][pos[1]])
            elif event.button == 3:  # Right click to deselect
                selected_piece = None
                valid_moves = None
   
    # Check game state
    in_check = is_in_check(board, current_player)
    in_checkmate = is_checkmate(board, current_player)
    in_stalemate = is_stalemate(board, current_player)
   
    # If game is over, show message and wait for restart
    if in_checkmate or in_stalemate:
        draw_board(screen, selected_piece, valid_moves, last_move)
        if in_checkmate:
            winner = 'Black' if current_player == 'white' else 'White'
            status_text = f"Checkmate! {winner} wins!"
        else:
            status_text = "Stalemate! Game is a draw!"
       
        font = pygame.font.SysFont('Arial', 48)
        text_surface = font.render(status_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(text_surface, text_rect)
       
        restart_text = font.render("Press R to restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50))
        screen.blit(restart_text, restart_rect)
    else:
        # If playing against AI, make AI move
        if current_player == 'black' and not ai_thinking and game_mode == 'ai':
            ai_thinking = True
            start_pos = None
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board[row][col] and board[row][col][0] == 'black':
                        start_pos = (row, col)
                        break
                if start_pos:
                    break
            make_ai_move(board)
            # Update last_move for AI moves
            if start_pos:
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        if board[row][col] and board[row][col][0] == 'black' and (row, col) != start_pos:
                            last_move = (start_pos, (row, col))
                            break
            current_player = 'white'
            ai_thinking = False
       
        # Draw the game state
        draw_board(screen, selected_piece, valid_moves, last_move)
        draw_game_status(screen, current_player, in_check, in_checkmate)
   
    show_fps(screen, clock)
    pygame.display.flip()
    clock.tick(FPS)
 
pygame.quit()
sys.exit()
 
 