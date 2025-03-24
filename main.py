import pygame
import sys
from data.classes.Board import Board

# Initialize Pygame
pygame.init()
window_size = (750, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Chess Game")

# Fonts and Colors
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER = (30, 130, 230)

class Button:
    """A simple button class for UI elements."""
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        """Draws the button."""
        color = BUTTON_HOVER if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
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
    """Displays the main menu."""
    start_button = Button("Start Game", window_size[0]//2 - 100, 300, 200, 60, main)
    quit_button = Button("Quit", window_size[0]//2 - 100, 400, 200, 60, sys.exit)
    while True:
        screen.fill(WHITE)
        draw_text("Chess Game", font, BLACK, screen, window_size[0]//2, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in [start_button, quit_button]:
                button.handle_event(event)
        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, quit_button]:
            button.check_hover(mouse_pos)
            button.draw(screen)
        pygame.display.update()

def pause_menu():
    """Pause menu that appears when ESC is pressed."""
    global paused
    paused = True  # Set paused state
    resume_button = Button("Resume", window_size[0]//2 - 100, 300, 200, 60, lambda: set_paused(False))
    quit_button = Button("Quit to Menu", window_size[0]//2 - 100, 400, 200, 60, main_menu)
    while paused:  # Stay in pause menu until unpaused
        screen.fill(WHITE)
        draw_text("Paused", font, BLACK, screen, window_size[0]//2, 200)
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

def set_paused(value):
    """Updates the paused state to resume the game."""
    global paused
    paused = value

def draw_text(text, font, color, surface, x, y):
    """Helper function to render text."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def initialize_game():
    """Initializes the game board."""
    board = Board(window_size[0], window_size[1])
    return board

def handle_events(board):
    """Handles user input, including ESC for pausing."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu()  # If the user closes the game, go to the main menu
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_menu()  # Open the pause menu
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            board.handle_click(mx, my)
    return True

def check_game_status(board):
    """Checks if the game has ended and returns the result."""
    if board.is_in_checkmate('black'):
        return "White Wins!"
    elif board.is_in_checkmate('white'):
        return "Black Wins!"
    elif only_kings_left(board):
        return "Draw! Only kings left."
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

def main():
    """Main game loop with pause functionality."""
    global paused
    paused = False  # Ensure the game starts unpaused
    board = initialize_game()
    running = True

    while running:
        running = handle_events(board)
        if not running:
            main_menu()  # If quitting mid-game, return to main menu
            break

        if paused:
            pause_menu()  # If paused, enter pause menu before continuing

        game_result = check_game_status(board)
        if game_result:
            main_menu()  # Return to menu instead of getting stuck

        draw(screen, board)

if __name__ == '__main__':
    main_menu()  # Start the game with the main menu