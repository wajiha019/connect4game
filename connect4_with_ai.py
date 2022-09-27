  
import numpy as np
import random
import pygame
import math


class Connect4_Game:

    def __init__(self):
        self.PURPLE = (255, 102, 204)
        self.WHITE = (255, 255, 255)
        self.BLUE = (145, 145, 255)
        self.GREEN = (145, 255, 145)

        self.ROW_COUNT = 6 
        self.COLUMN_COUNT = 7
        
#variables used for players turns
        self.PLAYER = 0
        self.AI = 1
        
#variables used for players piece value in the board
        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        

        self.WINDOW_LENGTH = 4 #used in score position function to create an array of four elements
        
        self.SQUARESIZE = 100 #100 pixcels in pygame window 
        self.width = self.COLUMN_COUNT * self.SQUARESIZE #screen width
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE #screen height
        
        self.size = (self.width, self.height)#screen size
        
        self.RADIUS = int(self.SQUARESIZE / 2 - 5) #radius of a circle in pygame window
        
        self.screen = pygame.display.set_mode(self.size) #pygame Window of size self.size
        
        
#creates 2D array board
    def create_board(self):
        board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT)) #Nmpy  2D array with values set as zero
        return board
    
    

#Set value of player's piece in the board
    def drop_piece(self,board, row, col, piece):
        board[row][col] = piece
        
        

#check whether the location is empty or not
    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT - 1][col] == 0
    
    

#returns the next row to drop piece in a particular column
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r
            
            

#Returns flip board because we want to represent rows from bottom to top
    def print_board(self, board):
        np.flip(board, 0)
        
        


#Returns true when we get consecutive player's piece in either horizontal,vertical 
#or negative or positive diagonals
    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece: #condition for four consecutive player's piece
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3): #Iterates through column 0 to 3
            for r in range(self.ROW_COUNT - 3): #iterates through row 0 to 2
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3): #Iterates through column 0 to 3
            for r in range(3, self.ROW_COUNT): #Iterates through row 3 t0 5
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True



#Return the score of a window which is the array of 4 pieces in either  horizontal,vertical 
#or negative or positive diagonals
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score



#returns score after iterating through board for a player's piece
    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])] #list of center column values
        center_count = center_array.count(piece)
        score += center_count * 3 # score in increamented by multiplying total pieces in centre row with 3

        ## Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])] #horizontal list of a row and its all columns values
            for c in range(self.COLUMN_COUNT - 3): 
                window = row_array[c:c + self.WINDOW_LENGTH] #list of 4 horizontal values
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])] #Vertical list of a column andits all rows values
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.WINDOW_LENGTH] #list of 4 vertical values
                score += self.evaluate_window(window, piece)

        ## Score positive sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)] # list 4 positive diagonal values
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)] #list of 4 negative diagonals
                score += self.evaluate_window(window, piece)

        return score



#returns the list of columns that have spaces to drop pieces
    
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):#iterate through every column
            if self.is_valid_location(board, col):#checks column is not full
                valid_locations.append(col)
        return valid_locations
    



#returns true when no more pieces are left to drop in the board or 
#when the AI player or human player wins the game.
    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(
            self.get_valid_locations(board)) == 0



#returns the best score and best column to drop the piece
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return None, 100000000000000   #None refers to column as we return column,value in later part of code
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, self.AI_PIECE) 
        if maximizingPlayer: #AI player
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy() # copy the same board to create a temporary, .copy creates board which points to different memory location so that our original board is not affected
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1] # second value of tuple returned by minimax i.e score
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player human player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
        
        

#Creates graphics of board
    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.PURPLE, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.WHITE, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if board[r][c] == self.PLAYER_PIECE:
                    pygame.draw.circle(self.screen, self.BLUE, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif board[r][c] == self.AI_PIECE:
                    pygame.draw.circle(self.screen, self.GREEN, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()



