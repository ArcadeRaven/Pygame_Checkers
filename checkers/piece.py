import pygame
from .constants import VIOLET, WHITE, GREY, SQUARE_SIZE, CROWN

class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color 
        self.king = False

        #if self.color == VIOLET:
        #    self.direction = -1 # pygame goes down, so going up is coded as negative
        #else:
        #    self.direction = 1 # going down is coded as positive

        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True 

    def draw (self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2)) # blit means put an image on the screen

    def move(self, row, col):
        self.row = row 
        self.col = col 
        self.calc_pos()
    
    def __repr__(self): # internal representation of the object
        return str(self.color)