import pygame

# Tile creator
class Square:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.abs_x, self.abs_y = x * width, y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.colour = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_colour = (220, 208, 194) if self.colour == 'light' else (53, 53, 53)
        self.highlight_colour = (100, 249, 83) if self.colour == 'light' else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    # get the formal notation of the tile
    def get_coord(self):
        return 'abcdefgh'[self.x] + str(self.y + 1)

    def draw(self, display):
        colour = self.highlight_colour if self.highlight else self.draw_colour
        pygame.draw.rect(display, colour, self.rect)
        if self.occupying_piece:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)