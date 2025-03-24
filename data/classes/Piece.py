import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x, self.y = pos
        self.color = color
        self.has_moved = False

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece:
                    if square.occupying_piece.color == self.color:
                        break
                    output.append(square)
                    break
                output.append(square)
        return output

    def get_valid_moves(self, board):
        return [square for square in self.get_moves(board) if not board.is_in_check(self.color, board_change=[self.pos, square.pos])]

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
        if self.notation == ' ' and (self.y == 0 or self.y == 7):
            from data.classes.pieces.Queen import Queen
            square.occupying_piece = Queen((self.x, self.y), self.color, board)
        if self.notation == 'K':
            if prev_square.x - self.x == 2:
                rook = board.get_piece_from_pos((0, self.y))
                rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
            elif prev_square.x - self.x == -2:
                rook = board.get_piece_from_pos((7, self.y))
                rook.move(board, board.get_square_from_pos((5, self.y)), force=True)

    def attacking_squares(self, board):
        return self.get_moves(board)