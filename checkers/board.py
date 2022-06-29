import imp
import pygame
from .constants import COLS, ROWS, VIOLET, WHITE, BLACK, SQUARE_SIZE
from .piece import Piece

class Board:
        def __init__(self):
                self.board = []
                self.violet_left = self.white_left = 12
                self.violet_kings = self.white_kings = 0
                self.create_board()

        def draw_squares(self, win):
                win.fill(BLACK)
                for row in range(ROWS):
                    for col in range (row % 2, ROWS, 2):
                        pygame.draw.rect(win, VIOLET, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) 
                        # rect argument, width and height. # draws from TL to BR. specify to draw 100 wide right and 100 long down, row, col, width, height

        def move(self, piece, row, col):
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] # swaps
            piece.move(row, col) # when moving piece, moves as row and col

            if row == ROWS - 1 or row == 0:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.violet_kings += 1

        def get_piece(self, row, col):
            return self.board[row][col]

        def create_board(self):
            for row in range(ROWS):
                self.board.append([]) # interior lists for each row
                for col in range(COLS):
                    if col % 2 == ((row + 1) % 2): # if cur col % 2 is= to row + 1 % 2, then draw violet or black square
                        if row < 3:
                            self.board[row].append(Piece(row, col, WHITE))
                        elif row > 4:
                            self.board[row].append(Piece(row, col, VIOLET)) # build board in rows > 4
                        else:
                            self.board[row].append(0) # blank piece
                    else:
                        self.board[row].append(0)

        def draw(self, win):
            self.draw_squares(win)
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col] #!
                    if piece != 0:
                        piece.draw(win)


        def remove(self, pieces):
            for piece in pieces:
                self.board[piece.row][piece.col] = 0
                if piece != 0:
                    if piece.color == VIOLET:
                        self.violet_left -= 1
                    else:
                        self.white_left -= 1

        def winner(self):
            if self.violet_left <= 0:
                return WHITE
            elif self.white_left <= 0:
                return VIOLET

            return None # if draw

        def get_valid_moves(self, piece):
            moves = {}
            left = piece.col - 1 # cause left 1
            right = piece.col + 1 # cause right one.
            # pygame goes top left to bot right.
            row = piece.row

            if piece.color == VIOLET or piece.king:
                moves.update(self._traverse_left(row - 1, max (row - 3, -1), -1, piece.color, left)) # traversing left
                moves.update(self._traverse_right(row - 1, max (row - 3, -1), -1, piece.color, right)) # traversing right

            if piece.color == WHITE or piece.king:
                moves.update(self._traverse_left(row + 1, min (row + 3, ROWS), 1, piece.color, left)) # traversing left
                moves.update(self._traverse_right(row + 1, min (row + 3, ROWS), 1, piece.color, right)) # traversing right

            # update move dictionary, then return it after moves
            return moves

        def _traverse_left(self, start, stop, step, color, left, skipped = []): # skipped checks if we have skipped pieces
            moves = {}
            last = []
            for r in range(start, stop, step): # for loop by row. r is counter for row
                if left < 0: # if no longer in range of our rows
                    break

                cur = self.board[r][left]
                if cur == 0: # if next is 0
                    if skipped and not last: # if skipped and last is undefined, then break cause there is something there, like trying to jump over 2 pieces, not gonna work.
                        break
                    elif skipped:
                        moves[(r, left)] = last + skipped # adds jump skip
                    else:
                        moves[(r, left)] = last # add as pos move
                    
                    if last: # if cur is 0 and last
                        if step == -1:
                            row = max(r - 3, 0)
                        else:
                            row = min(r + r, ROWS) # prep double jumb or triple jump

                        moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped = last)) # if step is -1, subs 1, if step is +1, add 1
                        moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped = last))
                    break

                elif cur.color == color:
                    break 

                else: last = [cur]

                left -= 1

            return moves


        def _traverse_right(self, start, stop, step, color, right, skipped = []):
            moves = {}
            last = []
            for r in range(start, stop, step): # for loop by row. r is counter for row
                if right >= COLS: # if no longer in range of our rows
                    break 
                
                cur = self.board[r][right]
                if cur == 0: # if next is 0
                    if skipped and not last: # if skipped and last is undefined, then break cause there is something there, like trying to jump over 2 pieces, not gonna work.
                        break
                    elif skipped:
                        moves[(r, right)] = last + skipped
                    else:
                        moves[(r, right)] = last # add as pos move
                    
                    if last: # if cur is 0 and last
                        if step == -1:
                            row = max(r - 3, 0)
                        else:
                            row = min(r + 3, ROWS) # prep double jumb or triple jump

                        moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped = last)) # if step is -1, subs 1, if step is +1, add 1
                        moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped = last))
                    break

                elif cur.color == color:
                    break 

                else:
                    last = [cur]

                right += 1

            return moves