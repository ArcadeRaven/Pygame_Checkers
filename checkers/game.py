# handles game and piece movement
import pygame
from .constants import VIOLET, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self): # updates display
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self): # _ makes it private
        self.selected = None 
        self.board = Board() # creates board for main
        self.turn = VIOLET
        self.valid_moves = {} # tells us current valid moves

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init(self)

    def select(self, row, col): # if selected piece, move. change selection if select diff piece
        if self.selected:
            result = self._move(row, col) # move is private. move to row and col
            if not result: # try to select a diff piece
                self.selected = None # get rid of cur selection
                self.select(row, col) # reselect new piece. recursive call func again
        
        piece = self.board.get_piece(row, col)
        if piece !=0 and piece.color == self.turn: # turn = turn it cur is 
            self.selected = piece 
            self.valid_moves = self.board.get_valid_moves(piece)
            return True 

        return False # if not true, return false


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col) # move selected piece to row and col
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True 

    def draw_valid_moves(self, moves):
        for move in moves: # move is keys in dict
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15) # 15 is radius


    def change_turn(self): # if violet, change to white and vice versa
        self.valid_moves = {}
        if self.turn == VIOLET:
            self.turn = WHITE 
        else:
            self.turn = VIOLET