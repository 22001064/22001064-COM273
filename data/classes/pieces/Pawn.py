import pygame
from data.classes.Piece import Piece
from data.classes.pieces.Queen import Queen
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = 'data/images/' + color[0] + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
        self.notation = 'P'
        self.has_moved = False  # Track whether the pawn has moved

    def get_possible_moves(self, board):
        output = []
        moves = []
        
        # Move forward
        if self.color == 'white':
            moves.append((0, -1))  # Regular move 1 square forward
            if not self.has_moved and self.y == 6:  # Allow 2-square move only if in the starting position
                moves.append((0, -2))  # Initial 2-square move for white
        elif self.color == 'black':
            moves.append((0, 1))  # Regular move 1 square forward
            if not self.has_moved and self.y == 1:  # Allow 2-square move only if in the starting position
                moves.append((0, 2))  # Initial 2-square move for black

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])

            # Ensure that the move is within bounds
            if 0 <= new_pos[1] < 8:
                target_square = board.get_square_from_pos(new_pos)
                # If the square is empty, add it to possible moves
                if target_square.occupying_piece is None:
                    output.append(target_square)

        return output

    def get_moves(self, board):
        output = []
        for square in self.get_possible_moves(board):
            if square.occupying_piece is None:
                output.append(square)
        
        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:  # Check diagonal capture for white
                square = board.get_square_from_pos((self.x + 1, self.y - 1))
                if square.occupying_piece and square.occupying_piece.color != self.color:
                    output.append(square)

            if self.x - 1 >= 0 and self.y - 1 >= 0:  # Check diagonal capture for white
                square = board.get_square_from_pos((self.x - 1, self.y - 1))
                if square.occupying_piece and square.occupying_piece.color != self.color:
                    output.append(square)

        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:  # Check diagonal capture for black
                square = board.get_square_from_pos((self.x + 1, self.y + 1))
                if square.occupying_piece and square.occupying_piece.color != self.color:
                    output.append(square)

            if self.x - 1 >= 0 and self.y + 1 < 8:  # Check diagonal capture for black
                square = board.get_square_from_pos((self.x - 1, self.y + 1))
                if square.occupying_piece and square.occupying_piece.color != self.color:
                    output.append(square)

        return output

    def attacking_squares(self, board):
        moves = self.get_moves(board)
        # Only return diagonal attack squares
        return [i for i in moves if i.x != self.x]

    def handle_special_moves(self, board, prev_square, square):
        # Pawn Promotion
        if self.notation == 'P' and (self.y == 0 or self.y == 7):  # Pawn reaches last rank
            promotion_piece = self.choose_promotion(board)
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
        BUTTON_COLOR = (50, 150, 255)
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
            text = font.render("Choose a piece:", True, BLACK)
            screen.blit(text, (x_center - text.get_width() // 2, y_start - 60))

            mouse_pos = pygame.mouse.get_pos()

            for name, piece_class, rect in buttons:
                color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(screen, color, rect, border_radius=10)
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
                            selected_piece = piece_class((self.x, self.y), self.color, board)
                            break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return Queen((self.x, self.y), self.color, board)  

        return selected_piece
    