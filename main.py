
from xml.etree.ElementTree import VERSION
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, VIOLET # from constants in checkers folder using the init.py inside the subfolder checkers
from checkers.board import Board
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos # uses x and y pos of mouse
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())

        for event in pygame.event.get(): # checks if events have happened, if so, then progress
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # for left mouse button down
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()
main()