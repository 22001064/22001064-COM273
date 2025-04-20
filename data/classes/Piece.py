import pygame

class Piece:
    def __init__(self, pos, colour, board, is_ai=False):
        self.pos = pos
        self.x, self.y = pos
        self.colour = colour
        self.board = board
        self.is_ai = is_ai  # Flag to check if it's AI's piece
        self.has_moved = False

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece:
                    if square.occupying_piece.colour == self.colour:
                        break
                    output.append(square)
                    break
                output.append(square)
        return output

    def get_valid_moves(self, board):
        return [square for square in self.get_moves(board) if not board.is_in_check(self.colour, board_change=[self.pos, square.pos])]

    def move(self, board, square, force=False):
        for sq in board.squares:
            sq.highlight = False
        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True
            self.handle_special_moves(board, prev_square, square)
            return True
        board.selected_piece = None
        return False

    def handle_special_moves(self, board, prev_square, square):
        # Pawn Promotion
        if self.notation == 'P' and (self.y == 0 or self.y == 7):  # Pawn reaches last rank
            promotion_piece = self.choose_promotion(board)  # Automatically promote if AI
            square.occupying_piece = promotion_piece  # Replace pawn with chosen piece
        # Castling
        if self.notation == 'K':
            if prev_square.x - self.x == 2:  # Queenside castling
                rook = board.get_piece_from_pos((0, self.y))
                rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
            elif prev_square.x - self.x == -2:  # Kingside castling
                rook = board.get_piece_from_pos((7, self.y))
                rook.move(board, board.get_square_from_pos((5, self.y)), force=True)

    def choose_promotion(self, board):
        """ AI decides on the promotion piece. """
        from data.classes.pieces.Queen import Queen
        if self.colour == 'white' and self.y == 7:  # For white, show the promotion screen
            return self.choose_promotion_ui(board)
        if self.colour == 'black' and self.y == 0:  # For black, automatically promote to Queen
            if self.is_ai == True: # AI chooses Queen
                return Queen((self.x, self.y), self.colour, board)
            elif self.is_ai == False: # Player chooses piece
                return self.choose_promotion_ui(board)

    def choose_promotion_ui(self, board):
        """ Opens a popup allowing the player to select a promotion piece. """
        import pygame
        from data.classes.pieces.Queen import Queen
        from data.classes.pieces.Rook import Rook
        from data.classes.pieces.Bishop import Bishop
        from data.classes.pieces.Knight import Knight

        screen = pygame.display.get_surface()
        if screen is None:
            raise RuntimeError("No active Pygame display surface found!")

        font = pygame.font.Font(None, 40)

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        BUTTON_colour = (50, 150, 255)
        BUTTON_HOVER = (30, 130, 230)

        # Define button positions
        button_width = 100
        button_height = 50
        x_center = screen.get_width() // 2
        y_start = screen.get_height() // 2 - 100


        pieces = [("Queen", Queen), ("Rook", Rook), ("Bishop", Bishop), ("Knight", Knight)]
        buttons = []
        
        for i, (name, piece_class) in enumerate(pieces):
            rect = pygame.Rect(x_center - 50, y_start + i * 60, button_width, button_height)
            buttons.append((name, piece_class, rect))

        selected_piece = None

        while selected_piece is None:
            screen.fill(WHITE)

            message_text = font.render("If it's not your piece press ESC", True, BLACK)
            prompt_text = font.render("Choose a piece:", True, BLACK)

            screen.blit(message_text, (x_center - message_text.get_width() // 2, y_start - 90))
            screen.blit(prompt_text, (x_center - prompt_text.get_width() // 2, y_start - 60))

            mouse_pos = pygame.mouse.get_pos()

            for name, piece_class, rect in buttons:
                colour = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_colour
                pygame.draw.rect(screen, colour, rect, border_radius=10)
                text_surf = font.render(name, True, WHITE)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for name, piece_class, rect in buttons:
                        if rect.collidepoint(event.pos):
                            selected_piece = piece_class((self.x, self.y), self.colour, board)
                            break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return Queen((self.x, self.y), self.colour, board)  

        return selected_piece

    def attacking_squares(self, board):
        return self.get_moves(board)
