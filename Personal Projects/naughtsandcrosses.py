'''
A simple tic tac toe game implemented with only functions
'''

from IPython.display import clear_output
import random

def display(game_list):

    print(f'{game_list[6]} | {game_list[7]} | {game_list[8]}')
    print('---------')
    print(f'{game_list[3]} | {game_list[4]} | {game_list[5]}')
    print('---------')
    print(f'{game_list[0]} | {game_list[1]} | {game_list[2]}')

def player_input():
    
    marker = 'placeholder'
    
    while marker not in ['X','O']:
        
        marker = input('Before you begin, please select X or O: ').upper()
        
        if marker not in ['X', 'O']:
            
            clear_output()
            print('Whoops, that\'s not a valid choice!')

    if marker == 'X':
        
        return ('X','O')
    
    else:
        
        return ('O','X')

def posit_choice(board):

    posit = 'placeholder'
    
    while posit not in ['1','2','3','4','5','6','7','8','9'] or not space_check(board,int(posit)):
        
        posit = input('Select where you would like to place your symbol (1-9): ')
         
        if posit not in ['1','2','3','4','5','6','7','8','9']:
                            
                clear_output()
                display(board)
                print('Hey, that\'s not part of the board!')
            
        elif not space_check(board,int(posit)):
                
                clear_output()
                display(board)
                print('Hey, you can\'t place there!')              
                                
    return int(posit)

def board_placement(game_board,position,playersymbol):
    
    game_board[position-1] = playersymbol

def choose_first():
    
    first = random.randint(0,1)
    
    if first == 0:
        
        return 'Player One'
    
    else:
        
        return 'Player Two'
    
def ready():
    
    choice = 'placeholder'
    
    while choice not in ['Y','N']:
        
        choice = input("Are you ready to begin? (Y or N) ").upper()
        
        if choice not in ['Y','N']:
            print("Sorry, I don\'t understand, please choose Y or N")

    if choice == 'Y':
        
        return True
    
    else:
        
        return False

def win_check(board, mark):
    
    return \
        board[0] == board[1] == board[2] == mark or \
        board[3] == board[4] == board[5] == mark or \
        board[6] == board[7] == board[8] == mark or \
        board[0] == board[3] == board[6] == mark or \
        board[1] == board[4] == board[7] == mark or \
        board[2] == board[5] == board[8] == mark or \
        board[0] == board[4] == board[8] == mark or \
        board[6] == board[4] == board[2] == mark
    
def space_check(board, position):
    
    return board[position-1] == ' '
    
def full_board_check(board):

    return not ' ' in board

def replay():
    
    choice = 'placeholder'
    
    while choice not in ['Y','N']:
        
        choice = input("Would you like to play again? (Y or N) ").upper()
        
        if choice not in ['Y','N']:
            
            clear_output()
            print("Sorry, I don\'t understand, please choose Y or N")

    if choice == "Y":
        
        return True
    
    else:
        
        return False
    
def naughtsandcrosses():
    
    while True:
        
        game_on = True
        game_board = [' ']*9
        
        print('Welcome to Monty Python\'s Naughts and Crosses! Please use the number pad to play.')
    
        playerone, playertwo = player_input()

        turn = choose_first()
            
        print(f'{turn}, you are going first.')
        
        if not ready():
            
            print('Goodbye!')
            break

        while game_on:
            
            if turn == 'Player One':
    
                clear_output()
                display(game_board)

                print(f'{turn}, it is your turn.')

                position = posit_choice(game_board)

                board_placement(game_board,position,playerone)

                if win_check(game_board,playerone):

                    clear_output()
                    display(game_board)
                    print(f'{turn} wins!')
                    game_on = False

                elif full_board_check(game_board):

                    clear_output()
                    display(game_board)
                    print('It\'s a tie!')
                    game_on = False
                    
                turn = 'Player Two'
                
            else:
                
                clear_output()
                display(game_board)
                      
                print(f'{turn}, it is your turn.')

                position = posit_choice(game_board)

                board_placement(game_board,position,playertwo)

                if win_check(game_board,playertwo):

                    clear_output()
                    display(game_board)
                    print(f'{turn} wins!')
                    game_on = False

                elif full_board_check(game_board):

                    clear_output()
                    display(game_board)
                    print('It\'s a tie!')
                    game_on = False
                    
                turn = 'Player One'
            
        if not replay():
            
            print('Goodbye!')
            break
            
naughtsandcrosses()
