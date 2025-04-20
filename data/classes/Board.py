import pygame
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn

class Board:
    def __init__(self, width, height, config=None):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = config if config else self.default_config()
        self.squares = self.generate_squares()
        self.setup_board()
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a_moved = False
        self.white_rook_h_moved = False
        self.black_rook_a_moved = False
        self.black_rook_h_moved = False
        self.en_passant_square = "-"  # target square after pawn moves two squares
        self.halfmove_clock = 0  # resets on pawn move or capture
        self.fullmove_number = 1  # increments after black's move

    def default_config(self):
        return [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

    def generate_squares(self):
        return [Square(x, y, self.tile_width, self.tile_height) for y in range(8) for x in range(8)]

    def get_square_from_pos(self, pos):
        return next(square for square in self.squares if (square.x, square.y) == pos)

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        piece_classes = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn}
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece:
                    square = self.get_square_from_pos((x, y))
                    piece_class = piece_classes[piece[1]]
                    square.occupying_piece = piece_class((x, y), 'white' if piece[0] == 'w' else 'black', self)

    def handle_click(self, mx, my):
        x, y = mx // self.tile_width, my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece and clicked_square.occupying_piece.colour == self.turn:
                self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'
        elif clicked_square.occupying_piece and clicked_square.occupying_piece.colour == self.turn:
            self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, colour, board_change=None):
        king_pos, changing_piece, old_square, new_square, new_square_old_piece = None, None, None, None, None
        if board_change:
            old_square, new_square = self.get_square_from_pos(board_change[0]), self.get_square_from_pos(board_change[1])
            changing_piece, new_square_old_piece = old_square.occupying_piece, new_square.occupying_piece
            old_square.occupying_piece, new_square.occupying_piece = None, changing_piece

        pieces = [square.occupying_piece for square in self.squares if square.occupying_piece]
        if changing_piece and changing_piece.notation == 'K':
            king_pos = new_square.pos
        if not king_pos:
            king_pos = next(piece.pos for piece in pieces if piece.notation == 'K' and piece.colour == colour)

        in_check = any(king_pos == square.pos for piece in pieces if piece.colour != colour for square in piece.attacking_squares(self))

        if board_change:
            old_square.occupying_piece, new_square.occupying_piece = changing_piece, new_square_old_piece
        return in_check

    def is_in_checkmate(self, colour):
        king = next(piece for piece in (square.occupying_piece for square in self.squares) if piece and piece.notation == 'K' and piece.colour == colour)
        return not king.get_valid_moves(self) and self.is_in_check(colour)

    def is_trapped(self, colour):
        """Check if the current player is trapped and can't move any piece."""
        pieces = [square.occupying_piece for square in self.squares if square.occupying_piece and square.occupying_piece.colour == colour]
        
        # Check if any piece has valid moves
        for piece in pieces:
            if piece.get_valid_moves(self):
                return False  # Player has a valid move, they are not trapped

        return True  # No valid moves for the player, they are trapped

    def draw(self, display):
        # Draw squares and highlight moves
        if self.selected_piece:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        for square in self.squares:
            square.draw(display)

        # Draw red outline around king in check (but not checkmate)
        for square in self.squares:
            piece = square.occupying_piece
            if piece and piece.notation == 'K':
                colour = piece.colour
                if self.is_in_check(colour) and not self.is_in_checkmate(colour):
                    pygame.draw.rect(display, (255, 0, 0), square.rect, 4)  # Red outline for check


    def get_fen(self):
        """Generates an updated FEN string based on the current board state."""
        board_state = [["" for _ in range(8)] for _ in range(8)]

        # Populate board_state from self.squares
        for square in self.squares:
            piece = square.occupying_piece
            if piece:
                symbol = piece.notation.upper() if piece.colour == "white" else piece.notation.lower()
                board_state[square.y][square.x] = symbol

        # Convert board_state into FEN format
        fen_rows = []
        for row in board_state:
            empty_count = 0
            fen_row = ""
            for cell in row:
                if cell == "":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += cell
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        piece_placement = "/".join(fen_rows)
        active_colour = "w" if self.turn == "white" else "b"
        castling = self.get_castling_rights()
        ep = self.en_passant_square
        half = self.halfmove_clock
        full = self.fullmove_number
        fen = f"{piece_placement} {active_colour} {castling} {ep} {half} {full}"
        
        # Debugging output
        print(f"Generated FEN: {fen}")
        return fen

    def get_castling_rights(self):
        rights = ''

        # Find pieces manually
        white_king = self.get_piece_from_pos((4, 7))
        white_rook_h = self.get_piece_from_pos((7, 7))
        white_rook_a = self.get_piece_from_pos((0, 7))
        black_king = self.get_piece_from_pos((4, 0))
        black_rook_h = self.get_piece_from_pos((7, 0))
        black_rook_a = self.get_piece_from_pos((0, 0))

        if white_king and white_king.notation == 'K' and not self.white_king_moved:
            if white_rook_h and white_rook_h.notation == 'R' and not self.white_rook_h_moved:
                rights += 'K'
            if white_rook_a and white_rook_a.notation == 'R' and not self.white_rook_a_moved:
                rights += 'Q'
        
        if black_king and black_king.notation == 'K' and not self.black_king_moved:
            if black_rook_h and black_rook_h.notation == 'R' and not self.black_rook_h_moved:
                rights += 'k'
            if black_rook_a and black_rook_a.notation == 'R' and not self.black_rook_a_moved:
                rights += 'q'

        return rights or '-'

    def move_piece(self, start_pos, end_pos):
        """Moves a piece on the board and updates FEN."""
        start_square = self.get_square_from_pos(start_pos)
        end_square = self.get_square_from_pos(end_pos)

        moving_piece = start_square.occupying_piece

        if not moving_piece:
            return None

        moved = moving_piece.move(self, end_square)
        if moved:
            # Update castling flags
            if moving_piece.notation == 'K':  # King moves
                if moving_piece.colour == 'white':
                    self.white_king_moved = True
                else:
                    self.black_king_moved = True
            elif moving_piece.notation == 'R':  # Rook moves
                if moving_piece.colour == 'white':
                    if start_pos == (0, 7):  # a1
                        self.white_rook_a_moved = True
                    elif start_pos == (7, 7):  # h1
                        self.white_rook_h_moved = True
                elif moving_piece.colour == 'black':
                    if start_pos == (0, 0):  # a8
                        self.black_rook_a_moved = True
                    elif start_pos == (7, 0):  # h8
                        self.black_rook_h_moved = True

            # Reset halfmove clock on pawn move or capture
            if moving_piece.notation == 'P' or end_square.occupying_piece:
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1

            # Set en passant target square
            if moving_piece.notation == 'P' and abs(start_pos[1] - end_pos[1]) == 2:
                ep_file = chr(ord('a') + start_pos[0])
                ep_rank = str((start_pos[1] + end_pos[1]) // 2)
                self.en_passant_square = f"{ep_file}{ep_rank}"
            else:
                self.en_passant_square = "-"
                
            # Increment fullmove number after black's move
            if self.turn == 'black':
                self.fullmove_number += 1

            # Update FEN after move
            new_fen = self.get_fen()
            print(f"Updated FEN: {new_fen}")  # Debugging output
            return new_fen
        return None

