import pygame
from data.classes.Board import Board

def initialize_game():
    pygame.init()
    window_size = (750, 700)
    screen = pygame.display.set_mode(window_size)
    board = Board(window_size[0], window_size[1])
    return screen, board

def handle_events(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            board.handle_click(mx, my)
    return True

def only_kings_left(board):
    pieces = [square.occupying_piece for square in board.squares if square.occupying_piece]
    return all(piece.notation == 'K' for piece in pieces)

def check_game_status(board):
    if board.is_in_checkmate('black'):
        print('White wins!')
        return False
    elif board.is_in_checkmate('white'):
        print('Black wins!')
        return False
    elif only_kings_left(board):
        print('Draw! Only kings left.')
        return False
    return True

def draw(display, board):
    display.fill('white')
    board.draw(display)
    pygame.display.update()

def main():
    screen, board = initialize_game()
    running = True
    while running:
        running = handle_events(board)
        if not running:
            break
        running = check_game_status(board)
        draw(screen, board)

if __name__ == '__main__':
    main()