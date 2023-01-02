# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable

import pandas as pd
from datetime import datetime, date
from os.path import exists

class Board:
    """
    This class creates a game board, prints it, and checks if it is full.
    """
    def __init__(self):
        self.grid = None
        self.full = False

    def new_board(self): # Create a new board
        self.grid = [
            [' ',' ',' '],
            [' ',' ',' '],
            [' ',' ',' ']
            ]
        return self.grid

    def print_board(self): # Print a board with numeric, contextual markers
        print('-' + '-' + '1' + '-' + '-' + '-' + '2' + '-' + '-' + '-' + '3' + '-')
        print('1 '+ self.grid[0][0] + ' | ' + self.grid[0][1] + ' | ' + self.grid[0][2])
        print('-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-')
        print('2 '+ self.grid[1][0] + ' | ' + self.grid[1][1] + ' | ' + self.grid[1][2])
        print('-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-' + '-')
        print('3 '+ self.grid[2][0] + ' | ' + self.grid[2][1] + ' | ' + self.grid[2][2])
        return

    def board_full(self, board): # Check for the board filling up
        for row in board:
            for position in row:
                if position == ' ':
                    return False
        return True

class Players:
    """
    This class is for managing players that play the game.
    """
    def __init__(self):
        self.first_player = None
        self.second_player = None

    def first_player_selection(self): # Get the starting player
        self.first_player = input("Will 'X' or 'O' start?")
        return self.first_player

    def validate_player_selection(self): # Validate the first player selection
        if self.first_player != 'X' and self.first_player != 'O':
            return False
        else:
            return True

    def get_first_player(self): # Get input from the player to define the first player
        self.first_player_selection()
        if self.validate_player_selection():
            return self.first_player
        else:
            while self.validate_player_selection() == False:
                print("Please make a valid selection of either 'X' or 'O'.")
                self.first_player_selection()

    def get_second_player(self): # Based on first player, define second player
        if self.first_player == 'X':
            self.second_player = 'O'
            return self.second_player
        else:
            self.second_player = 'X'
            return self.second_player

    def get_first_player_name(self): # Get the name of the first player
        self.first_player_name = input("Please enter the name of the first player.")
        if self.first_player_name:
            return self.first_player_name
        else:
            while self.first_player_name == '':
                print("Please enter a non-empty response.")
                self.first_player_name = input("Please enter the name of the first player.")

    def get_second_player_name(self): # Get the name of the second player
        self.second_player_name = input("Please enter the name of the second player.")
        if self.second_player_name:
            return self.second_player_name
        else:
            while self.second_player_name == '':
                print("Please enter a non-empty response.")
                self.second_player_name = input("Please enter the name of the second player.")

class PlayerType:
    """
    Establishes player types for Human vs. Human, Human vs. Bot, and Bot vs. Bot game setup
    """
    def input_player_type(self, player_number):  
        while True:
            try:
                self.player_type_input = int(input(f"{player_number} player type: Enter 1 for Human, 0 for Bot."))
            except ValueError:
                self.player_input_error = str("Please enter an integer value for player type.")
                continue
            else:
                #Exit the loop
                break

    def check_valid_player_type(self): # Validates the move input from users
        if self.player_type_input == 1 or self.player_type_input == 0:
            return True
        else:
            return False

    def set_player_type(self, player_number): # Combines input and validation
        self.input_player_type(player_number)

        if self.check_valid_player_type() == True:
            if self.player_type_input == 1:
                self.player_type = 'Human'
            elif self.player_type_input == 0:
                self.player_type = 'Bot'
            else:
                self.set_player_type(player_number)
        else:
            self.set_player_type(player_number)

    def get_player_type(self, cur_player_symbol, player_list): # Get user input for human or bot type
        if player_list[0][0] == cur_player_symbol:
            return player_list[0][1]
        else:
            return player_list[1][1]

    def get_player_name(self, cur_player_symbol, player_list): # Get the player's name
        if player_list[0][0] == cur_player_symbol:
            return player_list[0][2]
        else:
            return player_list[1][2]
            

class Human:
    """
    Defines human-specific behavior for the game.
    """
    def __init__(self):
        pass
    
    def get_move(self):  
        """
        Requests move input from users and ensures entries are numeric. If move input is
        not numeric, does not break the game and continues to request input.
        """
        while True:
            try:
                self.move_row = int(input("What row would you like to play in?"))
                self.move_col = int(input("What column would you like to play in?"))
            except ValueError:
                self.move_input_error = str("Please enter an integer value for row and column.")
                continue
            else:
                #Exit the loop
                break

    def check_valid_move(self, board): # Validates the move input from users
        if (self.move_row >= 1 and self.move_row <= 3) and (self.move_col >= 1 and self.move_col <= 3):
            if board[self.move_row-1][self.move_col-1] == ' ':
                return True
            self.error_message = "T"
            return False
        self.error_message = "B"
        return False

    def play_move(self, board, current_player): # Combines input and validation
        self.get_move()

        if self.check_valid_move(board):
            board[self.move_row - 1][self.move_col - 1] = current_player
            self.move = (self.move_row - 1, self.move_col - 1)
            return self.move
        else:
            self.play_move(board, current_player)

class Bot:
    """Bot-specific behavior."""
    def __init__(self):
        self.opponent = None

    def define_opponent(self, current_player):
        if current_player == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'
    
    def play_move(self, board, current_player):
        self.define_opponent(current_player)

        # RULE-BASED APPROACH LONG; REPLACE WITH LOOP LOGIC IF TIME ALLOWS
        # diag win
        if board[0][0] == board[2][2] == current_player and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[0][0] == board[1][1] == current_player and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[1][1] == board[2][2] == current_player and board[0][0] == ' ':
            board[0][0] = current_player    
            self.move = (0, 0)
            return self.move
        elif board[2][0] == board[0][2] == current_player and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[2][0] == board[1][1] == current_player and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        elif board[1][1] == board[0][2] == current_player and board[2][0] == ' ':
            board[2][0] = current_player
            self.move = (2, 0)
            return self.move

        # horizontal win
            # first row
        elif board[0][0] == board[0][1] == current_player and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        elif board[0][0] == board[0][2] == current_player and board[0][1] == ' ':
            board[0][1] = current_player
            self.move = (0, 1)
            return self.move
        elif board[0][1] == board[0][2] == current_player and board[0][0] == ' ':
            board[0][0] = current_player
            self.move = (0, 0)
            return self.move
            # second row
        elif board[1][0] == board[1][1] == current_player and board[1][2] == ' ':
            board[1][2] = current_player
            self.move = (1, 2)
            return self.move
        elif board[1][0] == board[1][2] == current_player and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[1][1] == board[1][2] == current_player and board[1][0] == ' ':
            board[1][0] = current_player
            self.move = (1, 0)
            return self.move
            # third row
        elif board[2][0] == board[2][1] == current_player and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[2][0] == board[2][2] == current_player and board[2][1] == ' ':
            board[2][1] = current_player
            self.move = (2, 1)
            return self.move
        elif board[2][1] == board[2][2] == current_player and board[2][0] == ' ':
            board[2][0] = current_player    
            self.move = (2, 0)
            return self.move
        # vertical win
            # first col
        elif board[0][0] == board[1][0] == current_player and board[2][0] == ' ':
            board[2][0] = current_player
            self.move = (2, 0)
            return self.move
        elif board[0][0] == board[2][0] == current_player and board[1][0] == ' ':
            board[1][0] = current_player
            self.move = (1, 0)
            return self.move
        elif board[1][0] == board[2][0] == current_player and board[0][0] == ' ':
            board[0][0] = current_player
            self.move = (0, 0)
            return self.move
            # second col
        elif board[0][1] == board[1][1] == current_player and board[2][1] == ' ':
            board[2][1] = current_player
            self.move = (2, 1)
            return self.move
        elif board[0][1] == board[2][1] == current_player and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[1][1] == board[2][1] == current_player and board[0][1] == ' ':
            board[0][1] = current_player
            self.move = (0, 1)
            return self.move
            # third col
        elif board[0][2] == board[1][2] == current_player and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[0][2] == board[2][2] == current_player and board[1][2] == ' ':
            board[1][2] = current_player
            self.move = (1, 2)
            return self.move
        elif board[1][2] == board[2][2] == current_player and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move

        # diag block
        elif board[0][0] == board[2][2] == self.opponent and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[0][0] == board[1][1] == self.opponent and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[1][1] == board[2][2] == self.opponent and board[0][0] == ' ':
            board[0][0] = current_player    
            self.move = (0, 0)
            return self.move
        elif board[2][0] == board[0][2] == self.opponent and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[2][0] == board[1][1] == self.opponent and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        elif board[1][1] == board[0][2] == self.opponent and board[2][0] == ' ':
            board[2][0] = current_player
            self.move = (2, 0)
            return self.move
        # horizontal block
            # first row
        elif board[0][0] == board[0][1] == self.opponent and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        elif board[0][0] == board[0][2] == self.opponent and board[0][1] == ' ':
            board[0][1] = current_player
            self.move = (0, 1)
            return self.move
        elif board[0][1] == board[0][2] == self.opponent and board[0][0] == ' ':
            board[0][0] = current_player
            self.move = (0, 0)
            return self.move
            # second row
        elif board[1][0] == board[1][1] == self.opponent and board[1][2] == ' ':
            board[1][2] = current_player
            self.move = (1, 2)
            return self.move
        elif board[1][0] == board[1][2] == self.opponent and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[1][1] == board[1][2] == self.opponent and board[1][0] == ' ':
            board[1][0] = current_player
            self.move = (1, 0)
            return self.move
            # third row
        elif board[2][0] == board[2][1] == self.opponent and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[2][0] == board[2][2] == self.opponent and board[2][1] == ' ':
            board[2][1] = current_player
            self.move = (2, 1)
            return self.move
        elif board[2][1] == board[2][2] == self.opponent and board[2][0] == ' ':
            board[2][0] = current_player    
            self.move = (2, 0)
            return self.move
        # vertical block
            # first col
        elif board[0][0] == board[1][0] == self.opponent and board[2][0] == ' ':
            board[2][0] = current_player
            self.move = (2, 0)
            return self.move
        elif board[0][0] == board[2][0] == self.opponent and board[1][0] == ' ':
            board[1][0] = current_player
            self.move = (1, 0)
            return self.move
        elif board[1][0] == board[2][0] == self.opponent and board[0][0] == ' ':
            board[0][0] = current_player
            self.move = (0, 0)
            return self.move
            # second col
        elif board[0][1] == board[1][1] == self.opponent and board[2][1] == ' ':
            board[2][1] = current_player
            self.move = (2, 1)
            return self.move
        elif board[0][1] == board[2][1] == self.opponent and board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[1][1] == board[2][1] == self.opponent and board[0][1] == ' ':
            board[0][1] = current_player
            self.move = (0, 1)
            return self.move
            # third col
        elif board[0][2] == board[1][2] == self.opponent and board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[0][2] == board[2][2] == self.opponent and board[1][2] == ' ':
            board[1][2] = current_player
            self.move = (1, 2)
            return self.move
        elif board[1][2] == board[2][2] == self.opponent and board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        # Normal moves
        elif board[0][0] == ' ':
            board[0][0] = current_player
            self.move = (0, 0)
            return self.move
        elif board[2][2] == ' ':
            board[2][2] = current_player
            self.move = (2, 2)
            return self.move
        elif board[2][0] == ' ':
            board[2][0] = current_player
            self.move = (2, 0)
            return self.move
        elif board[1][0] == ' ':
            board[1][0] = current_player
            self.move = (1, 0)
            return self.move
        elif board[2][1] == ' ':
            board[2][1] = current_player
            self.move = (2, 1)
            return self.move
        elif board[0][2] == ' ':
            board[0][2] = current_player
            self.move = (0, 2)
            return self.move
        elif board[1][1] == ' ':
            board[1][1] = current_player
            self.move = (1, 1)
            return self.move
        elif board[0][1] == ' ':
            board[0][1] = current_player
            self.move = (0, 1)
            return self.move
        elif board[1][2] == ' ':
            board[1][2] = current_player
            self.move = (1, 2)
            return self.move

class Moves:
    """
    This class gets and analyzes moves to ensure validity.
    """
    def __init__(self):
        self.move_row = None
        self.move_col = None
        self.diag_values_top_left = []
        self.diag_values_top_right = []
        self.winning_symbol = None
        self.winner = False
    
    def advance_turn(self, current_player): # Advances the turn to the other player
        if current_player == 'X':
            return 'O'
        else:
            return 'X'
    
    
    def check_for_win(self, board): # Game winning conditions
        if board[0][0] == board[0][1] == board [0][2] and board[0][0] != ' ':
            self.winner = True
            return  self.winner
        elif board[1][0] == board[1][1] == board [1][2] and board[1][0] != ' ':
            self.winner = True
            return  self.winner
        elif board[2][0] == board[2][1] == board [2][2] and board[2][0] != ' ':
            self.winner = True
            return  self.winner
        elif board[0][0] == board[1][0] == board [2][0] and board[0][0] != ' ':
            self.winner = True
            return  self.winner
        elif board[0][1] == board[1][1] == board [2][1] and board[0][1] != ' ':
            self.winner = True
            return  self.winner
        elif board[0][2] == board[1][2] == board [2][2] and board[0][2] != ' ':
            self.winner = True
            return  self.winner
        elif board[0][0] == board[1][1] == board [2][2] and board[0][0] != ' ':
            self.winner = True
            return  self.winner
        elif board[2][0] == board[1][1] == board [0][2] and board[2][0] != ' ':
            self.winner = True
            return  self.winner
        else:
            self.winner = False
            return self.winner

class DataHandling():
    """
    Handles data from and to csv files.
    """
    def __init__(self, game_file, move_file):
        self.game_file = game_file
        self.move_file = move_file
        if (exists(self.game_file)):
            self.game_data = pd.read_csv(self.game_file)
        else:
            self.game_data = pd.DataFrame(columns=[
                "Timestamp",
                "Player 1 Name",
                "Player 1 Symbol",
                "Player 1 Type",
                "Player 2 Name",
                "Player 2 Symbol",
                "Player 2 Type",
                "Winner",
                "Move Count",
            ])
        if (exists(self.move_file)):
            self.move_data = pd.read_csv(self.move_file)
        else:
            self.move_data = pd.DataFrame(columns=[
                "Game ID",
                "Move Number",
                "Player Name",
                "Player Type",
                "Player Symbol",
                "Board Position",
            ])
    
    def record_game_data(self, is_winner, p1_name, p1_symbol, p1_type, p2_name, p2_symbol, p2_type, winner, move_count):
        self.game_data.loc[len(self.game_data)] = {
                "Game ID": len(self.game_data),
                "Timestamp": datetime.now(),
                "Player 1 Name": p1_name,
                "Player 1 Symbol": p1_symbol,
                "Player 1 Type": p1_type,
                "Player 2 Name": p2_name,
                "Player 2 Symbol": p2_symbol,
                "Player 2 Type": p2_type,
                "Winner": winner if is_winner == True else "None-Draw",
                "Move Count": move_count,
            }
        self.game_data.to_csv(self.game_file, index=False)
        

    # NEED TO ADD GAME ID:
    def record_move_data(self, move_num, player_name, player_type, player_symbol, board_position):
        self.move_data.loc[len(self.move_data)] = {
                "Game ID": len(self.game_data),
                "Move Number": move_num,
                "Player Name": player_name,
                "Player Type": player_type,
                "Player Symbol": player_symbol,
                "Board Position": board_position,
        }
        self.move_data.to_csv(self.move_file, index=False)

class DataViz:
    """
    Visualize game data.
    """
    def __init__(self, game_data):
        self.game_data = game_data
        self.win_data = self.game_data[self.game_data["Winner"] != "None-Draw"]
        self.win_data_p1 = self.win_data[self.win_data["Player 1 Symbol"] == self.win_data["Winner"]]
        self.win_data_p1 = self.win_data_p1[["Player 1 Name", "Player 1 Symbol", "Player 1 Type"]]
        self.win_data_p1 = self.win_data_p1.rename(columns={"Player 1 Name": "Player Name", "Player 1 Symbol": "Player Symbol", "Player 1 Type": "Player Type"})
        self.win_data_p2 = self.win_data[self.win_data["Player 2 Symbol"] == self.win_data["Winner"]]
        self.win_data_p2 = self.win_data_p2[["Player 2 Name", "Player 2 Symbol", "Player 2 Type"]]
        self.win_data_p2 = self.win_data_p2.rename(columns={"Player 2 Name": "Player Name", "Player 2 Symbol": "Player Symbol", "Player 2 Type": "Player Type"})
        self.win_data_all = pd.concat([self.win_data_p1, self.win_data_p2])

    def wins_by_player(self):
        return self.win_data_all.groupby(["Player Name", "Player Type"], sort=True)["Player Symbol"].count().sort_values(ascending = False)

    def move_count_avg(self):
        return self.win_data["Move Count"].mean()

    def wins_by_type(self):
        self.win_data_by_type = self.win_data_all.groupby(["Player Type"], sort=True)["Player Symbol"].count().sort_values(ascending = False)        
        self.win_data_by_type.plot.bar(x="Player Type", rot=0)
