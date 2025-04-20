import pygame
import sys
import time
import pyperclip
from data.classes.Board import Board
from engine import get_best_move

# Initialise Pygame
pygame.init()
window_size = (750, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Chess Game")

# Load Images for AI and Player vs Player mode
ai_icon = pygame.image.load("data/images/ai_icon.png")
pvp_icon = pygame.image.load("data/images/pvp_icon.png")

# Resize images to fit buttons
ICON_SIZE = 40
ai_icon = pygame.transform.scale(ai_icon, (ICON_SIZE, ICON_SIZE))
pvp_icon = pygame.transform.scale(pvp_icon, (ICON_SIZE, ICON_SIZE))

# Fonts and Colours
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOUR = (50, 150, 255)
BUTTON_HOVER = (30, 130, 230)

current_game_mode = "pvp"
current_preset = None
current_fen = None


class Button:
    """A simple button class for UI elements."""
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = BUTTON_COLOUR
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        """Draws the button."""
        colour = BUTTON_HOVER if self.hovered else self.colour
        pygame.draw.rect(screen, colour, self.rect, border_radius=10)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        """Checks if the mouse is hovering over the button."""
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """Handles button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()

def main_menu():
    """Displays the main menu with game mode selection."""
    
    # Define buttons
    start_ai_button = Button("AI Mode", window_size[0]//2 - 150, 260, 300, 60, lambda: main(game_mode="ai"))
    preset_ai_button = Button("AI Preset", window_size[0]//2 - 150, 330, 300, 60, preset_menu_ai)
    start_pvp_button = Button("2-Player Mode", window_size[0]//2 - 150, 400, 300, 60, lambda: main(game_mode="pvp"))
    preset_pvp_button = Button("PVP Preset", window_size[0]//2 - 150, 470, 300, 60, preset_menu_pvp)
    quit_button = Button("Quit", window_size[0]//2 - 100, 550, 200, 50, sys.exit)
    board = Board(window_size[0], window_size[1])

    while True:
        board.draw(screen)
        draw_text("Chess Game", font, WHITE, screen, window_size[0]//2, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in [start_ai_button, preset_ai_button, start_pvp_button, preset_pvp_button, quit_button]:
                button.handle_event(event)

        # Handle hover effects and draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in [start_ai_button, preset_ai_button, start_pvp_button, preset_pvp_button, quit_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)

        def draw_icon(icon, button):
            icon_x = button.rect.x + 10
            icon_y = button.rect.y + (button.rect.height // 2) - (ICON_SIZE // 2)
            screen.blit(icon, (icon_x, icon_y))

        draw_icon(ai_icon, start_ai_button)  # AI Icon
        draw_icon(ai_icon, preset_ai_button)  # AI Icon
        draw_icon(pvp_icon, start_pvp_button)  # PVP Icon
        draw_icon(pvp_icon, preset_pvp_button)  # PVP Icon

        pygame.display.update()

def preset_menu_ai():
    """Preset menu for AI mode."""
    start_button = Button("Start Game", window_size[0]//2 - 150, 250, 300, 60, lambda: main("ai", preset="start"))
    mid_button = Button("Mid Game", window_size[0]//2 - 150, 330, 300, 60, lambda: main("ai", preset="mid"))
    end_button = Button("End Game", window_size[0]//2 - 150, 410, 300, 60, lambda: main("ai", preset="end"))
    fen_button = Button("Custom FEN", window_size[0]//2 - 150, 490, 300, 60, fen_input_screen)
    back_button = Button("Back", window_size[0]//2 - 100, 560, 200, 60, main_menu)
    board = Board(window_size[0], window_size[1])

    while True:
        board.draw(screen)
        draw_text("AI Preset Menu", font, WHITE, screen, window_size[0]//2, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in [start_button, mid_button, end_button, fen_button, back_button]:
                button.handle_event(event)

        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, mid_button, end_button, fen_button, back_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.update()

def preset_menu_pvp():
    """Preset menu for Player vs Player mode."""
    start_button = Button("Start Game", window_size[0]//2 - 150, 250, 300, 60, lambda: main("pvp", preset="start"))
    mid_button = Button("Mid Game", window_size[0]//2 - 150, 330, 300, 60, lambda: main("pvp", preset="mid"))
    end_button = Button("End Game", window_size[0]//2 - 150, 410, 300, 60, lambda: main("pvp", preset="end"))
    back_button = Button("Back", window_size[0]//2 - 100, 490, 200, 60, main_menu)
    board = Board(window_size[0], window_size[1])

    while True:
        board.draw(screen)

        draw_text("PVP Preset Menu", font, WHITE, screen, window_size[0]//2, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in [start_button, mid_button, end_button, back_button]:
                button.handle_event(event)

        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, mid_button, end_button, back_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.update()

def fen_input_screen():
    """Allows the user to input a custom FEN string with live preview."""
    input_box = pygame.Rect(window_size[0]//2 - 250, 300, 500, 50)
    user_text = ''
    error_message = ''
    active = True

    def is_valid_fen(fen):
        parts = fen.strip().split()
        return len(parts) == 6 and all(parts)

    preview_board = Board(window_size[0] // 2, window_size[1] // 2)
    valid_preview = False

    while active:
        screen.fill(WHITE)
        draw_text("Enter Custom FEN:", font, BLACK, screen, window_size[0]//2, 40)
        pygame.draw.rect(screen, BLACK, input_box, 2)

        font_input = pygame.font.Font(None, 28)
        text_surface = font_input.render(user_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        input_box.w = max(500, text_surface.get_width() + 20)

        # Try to render the FEN as a preview
        try:
            preview_board.set_fen(user_text)
            valid_preview = True
        except Exception as e:
            valid_preview = False

        if valid_preview:
            preview_board.draw(screen)
        elif user_text.strip():
            draw_text("Invalid FEN preview", small_font, (200, 0, 0), screen, window_size[0]//2, 120)

        if error_message:
            draw_text(error_message, small_font, (200, 0, 0), screen, window_size[0]//2, 370)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_valid_fen(user_text):
                        main(game_mode='ai', fen=user_text)
                        active = False
                    else:
                        error_message = "Invalid FEN. Please enter a full valid FEN string."
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    preset_menu_ai()
                    return
                else:
                    user_text += event.unicode

        pygame.display.update()

def pause_menu(board_surface=None):
    """Pause menu that appears when ESC is pressed."""
    global paused
    paused = True  # Set paused state
    resume_button = Button("Resume", window_size[0]//2 - 100, 300, 200, 60, lambda: set_paused(False))
    quit_button = Button("Quit to Menu", window_size[0]//2 - 100, 400, 200, 60, main_menu)
    while paused:  # Stay in pause menu until unpaused
        if board_surface:
            screen.blit(board_surface, (0, 0))  # Show the frozen board
        else:
            screen.fill(WHITE)
        draw_text("Paused", font, WHITE, screen, window_size[0]//2, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                set_paused(False)  # Resume game if ESC is pressed again
            for button in [resume_button, quit_button]:
                button.handle_event(event)
        mouse_pos = pygame.mouse.get_pos()
        for button in [resume_button, quit_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)
        pygame.display.update()

def end_screen(message, time_str, final_board_surface=None, last_move=None):
    """Displays the end screen with game results and buttons."""
    restart_button = Button("Restart", window_size[0]//2 - 100, 350, 200, 60, restart_game)
    menu_button = Button("Main Menu", window_size[0]//2 - 100, 420, 200, 60, main_menu)
    quit_button = Button("Quit", window_size[0]//2 - 100, 490, 200, 60, quit_game)
    
    # Create a transparent grey overlay
    overlay = pygame.Surface(window_size)
    overlay.set_alpha(100)  # Transparency (0 = fully transparent, 255 = opaque)
    overlay.fill((50, 50, 50))  # Grey colour

    while True:
        if final_board_surface:
            screen.blit(final_board_surface, (0, 0))
            screen.blit(overlay, (0, 0))

            if last_move and ("Wins" in message):  # Only highlights the piece that won the game if someone won
                start, end = last_move
                tile_width = window_size[0] // 8
                tile_height = window_size[1] // 8
                highlight_colour = (255, 215, 0)

                for pos in [start, end]:
                    rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
                    pygame.draw.rect(screen, highlight_colour, rect, 5)  # 5px outline
        else:
            screen.fill(WHITE)

        draw_text(message, font, WHITE, screen, window_size[0]//2, 250)
        draw_text(time_str, small_font, WHITE, screen, window_size[0]//2, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()  # Ensures proper quitting

            for button in [restart_button, menu_button, quit_button]:
                button.handle_event(event)

        mouse_pos = pygame.mouse.get_pos()
        for button in [restart_button, menu_button, quit_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.update()

def quit_game():
    """Returns to the main menu."""
    sys.exit()

def restart_game():
    """Restarts the game by reinitialising the board."""
    main(current_game_mode, current_preset, current_fen)

def set_paused(value):
    """Updates the paused state to resume the game."""
    global paused
    paused = value

def draw_text(text, font, colour, surface, x, y):
    """Helper function to render text."""
    text_obj = font.render(text, True, colour)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def initialise_game(config=None):
    """Initialises the game board."""
    board = Board(window_size[0], window_size[1], config)
    return board

def handle_events(board):
    """Handles user input, including ESC for pausing."""
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu()  # If the user closes the game, go to the main menu
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Open the pause menu if ESC is pressed
                board_surface = screen.copy()
                pause_menu(board_surface)  # Pass current board snapshot
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            board.handle_click(mx, my)
    return True

def check_game_status(board):
    """Checks if the game has ended and returns the result."""
    if board.is_in_checkmate('black'):
        return "White Wins!"
    elif board.is_in_checkmate('white'):
        return "Black Wins!"
    elif not board.is_in_check('black') and board.is_trapped('black') or not board.is_in_check('white') and board.is_trapped('white'):
        return "Draw! (Stalemate)"
    elif only_kings_left(board):
        return "Draw! Only Kings Left."
    return None  # Game still ongoing

def only_kings_left(board):
    """Checks if only kings remain (stalemate)."""
    pieces = [square.occupying_piece for square in board.squares if square.occupying_piece]
    return all(piece.notation == 'K' for piece in pieces)

def draw(display, board):
    """Draws the game board."""
    display.fill(WHITE)
    board.draw(display)
    pygame.display.update()

def main(game_mode="pvp", preset=None, fen=None):
    """Main game loop with AI or Player mode selection."""
    global paused
    global current_game_mode, current_preset, current_fen
    current_game_mode = game_mode
    current_preset = preset
    current_fen = fen
    paused = False  # Ensure the game starts unpaused
    start_time = time.time()
    board = initialise_game()
    last_move = None  # Track the last move for AI
    # inside main()
    if fen:
        board = initialise_game()
        board.set_fen(fen)
    elif preset == "mid":
        config = [
            ["", "", "", "", "bK", "", "", ""],
            ["", "bP", "", "", "", "bR", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "wP", "", ""],
            ["", "", "", "wB", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "wK", "", "", ""],
        ]
        board = initialise_game(config=config)
    elif preset == "end":
        config = [
            ["bR", "", "", "", "bK", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "wK", "", "", "wR"],
        ]
        board = initialise_game(config=config)
    else:
        board = initialise_game()

    fen_string = board.get_fen()
    pyperclip.copy(fen_string)
    print(f"FEN copied to clipboard: {fen_string}")
    running = True

    # Print selected game mode for debugging
    print(f"Game Mode: {game_mode}")

    while running:
        running = handle_events(board)
        if not running:
            main_menu()  # If quitting mid-game, return to main menu
            break

        if paused:
            pause_menu()  # If paused, enter pause menu before continuing

        game_result = check_game_status(board)
        if game_result:
            draw(screen, board)
            pygame.display.update()
            final_board_surface = screen.copy()
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f"Game Duration: {minutes}m {seconds}s"
            end_screen(game_result, time_str, final_board_surface, last_move)  # Show end screen with game result

        draw(screen, board)

        # If AI Mode, add AI move logic
        if game_mode == "ai" and board.turn == "black":  
            time.sleep(0.5)
            best_move = get_best_move(board)
            if best_move:
                try:
                    start_pos = (ord(best_move[0]) - ord('a'), 8 - int(best_move[1]))
                    end_pos = (ord(best_move[2]) - ord('a'), 8 - int(best_move[3]))
                    print(f"AI moving from {start_pos} to {end_pos}")
                    success = board.move_piece(start_pos, end_pos)
                    if success:
                        board.turn = 'white'  # Switch turn to player after AI move
                        last_move = (start_pos, end_pos)
                    else:
                        print("AI move failed")
                except Exception as e:
                    print(f"AI Move Error: {e}")  # Debugging message

if __name__ == '__main__':
    main_menu()  # Start the game with the main menu