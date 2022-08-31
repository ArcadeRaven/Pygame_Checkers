import pygame 

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb color vals
VIOLET = (71, 10, 12)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (48, 213, 200)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))
