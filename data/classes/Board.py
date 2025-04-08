from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = self.default_config()
        self.squares = self.generate_squares()
        self.setup_board()

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
            if clicked_square.occupying_piece and clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'
        elif clicked_square.occupying_piece and clicked_square.occupying_piece.color == self.turn:
            self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color, board_change=None):
        king_pos, changing_piece, old_square, new_square, new_square_old_piece = None, None, None, None, None
        if board_change:
            old_square, new_square = self.get_square_from_pos(board_change[0]), self.get_square_from_pos(board_change[1])
            changing_piece, new_square_old_piece = old_square.occupying_piece, new_square.occupying_piece
            old_square.occupying_piece, new_square.occupying_piece = None, changing_piece

        pieces = [square.occupying_piece for square in self.squares if square.occupying_piece]
        if changing_piece and changing_piece.notation == 'K':
            king_pos = new_square.pos
        if not king_pos:
            king_pos = next(piece.pos for piece in pieces if piece.notation == 'K' and piece.color == color)

        in_check = any(king_pos == square.pos for piece in pieces if piece.color != color for square in piece.attacking_squares(self))

        if board_change:
            old_square.occupying_piece, new_square.occupying_piece = changing_piece, new_square_old_piece
        return in_check

    def is_in_checkmate(self, color):
        king = next(piece for piece in (square.occupying_piece for square in self.squares) if piece and piece.notation == 'K' and piece.color == color)
        return not king.get_valid_moves(self) and self.is_in_check(color)

    def draw(self, display):
        if self.selected_piece:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)

    def get_fen(self):
        """Generates an updated FEN string based on the current board state."""
        board_state = [["" for _ in range(8)] for _ in range(8)]

        # Populate board_state from self.squares
        for square in self.squares:
            piece = square.occupying_piece
            if piece:
                symbol = piece.notation.upper() if piece.color == "white" else piece.notation.lower()
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
        active_color = "w" if self.turn == "white" else "b"
        castling_rights = "KQkq"  # Placeholder (implement castling logic)
        en_passant = "-"  # Placeholder (implement en passant tracking)
        halfmove_clock = "0"  # Placeholder (implement halfmove tracking)
        fullmove_number = "1"  # Placeholder (implement fullmove tracking)

        return f"{piece_placement} {active_color} {castling_rights} {en_passant} {halfmove_clock} {fullmove_number}"


    def move_piece(self, start_pos, end_pos):
        """Moves a piece on the board and updates FEN."""
        start_square = self.get_square_from_pos(start_pos)
        end_square = self.get_square_from_pos(end_pos)

        if start_square.occupying_piece:
            moved = start_square.occupying_piece.move(self, end_square)
            if moved:
                # Update the board state and FEN after a valid move
                new_fen = self.get_fen()
                print(f"Updated FEN: {new_fen}")  # Debugging output
                return new_fen
        return None
