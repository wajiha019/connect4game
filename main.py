import connect4_with_ai
import random
import pygame
import sys
import math


Game = connect4_with_ai.Connect4_Game() #Instantiate Connect4_game object
board = Game.create_board()
Game.print_board(board)


#Gmae graphics
pygame.init()
pygame.display.set_caption("FOUR in a ROW")#title of game on top of screen
# icon = pygame.image.load("icon.png")
# pygame.display.set_icon(icon)#icon on top of screen

Game.draw_board(board)
pygame.display.update() #updates the screen ,necessary after making changes to pygame screen

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(Game.PLAYER, Game.AI) #game initilizes with random player

game_over = False
while not game_over:# breaks when game is over

#iterates through every event of human player
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        if event.type == pygame.MOUSEMOTION: #when mouse is hovering over screen
            pygame.draw.rect(Game.screen, Game.WHITE, (0, 0, Game.width, Game.SQUARESIZE)) #Rectangle at top of screen where piece appears to drop
            posx = event.pos[0] #horizontal(x-axis) position of screen 
            if turn == Game.PLAYER:
                pygame.draw.circle(Game.screen, Game.BLUE, (posx, int(Game.SQUARESIZE / 2)), Game.RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: #when user clicks on the screen to drop the piece
            pygame.draw.rect(Game.screen, Game.WHITE, (0, 0, Game.width, Game.SQUARESIZE))
            
            # Ask for Player 1 Input
            if turn == Game.PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / Game.SQUARESIZE)) # x-axis position divided by hundred and then floor function is applied then type casted to integer

                if Game.is_valid_location(board, col): #droping piece
                    row = Game.get_next_open_row(board, col)
                    Game.drop_piece(board, row, col, Game.PLAYER_PIECE)

                    if Game.winning_move(board, Game.PLAYER_PIECE): #when player wins
                        label = myfont.render("YOU won!!", 1, Game.BLUE)
                        Game.screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2 # turn is either 0 or 1

                    Game.print_board(board)
                    Game.draw_board(board)

    #AI player turn
    if turn == Game.AI and not game_over:

       
        col, minimax_score = Game.minimax(board, 5, -math.inf, math.inf, True)

        if Game.is_valid_location(board, col):
            row = Game.get_next_open_row(board, col)
            Game.drop_piece(board, row, col, Game.AI_PIECE)

            if Game.winning_move(board, Game.AI_PIECE):
                label = myfont.render("YOU lost :(", 1, Game.GREEN)
                Game.screen.blit(label, (40, 10))
                game_over = True

            Game.print_board(board)
            Game.draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000) #waits 3000 miliseconds before exiting
        
        