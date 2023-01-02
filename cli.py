# # This file contains the Command Line Interface (CLI) for
# # the Tic-Tac-Toe game. This is where input and output happens.
# # For core game logic, see logic.py.

import pandas as pd
from logic import Players, Board, Moves, PlayerType, Human, Bot, DataHandling, DataViz

# Run the game from the CLI based on logic.py code:
class RunGame:
    """
    Establishes initial variables for gameplay. 
    """
    def __init__(self):
        self.players = Players()
        self.first_player = self.players.get_first_player()
        self.current_player = self.first_player
        self.first_player_name = self.players.get_first_player_name()
        self.get_first_player_type = PlayerType()
        self.get_first_player_type.set_player_type("First")
        self.first_player_type = self.get_first_player_type.player_type
        self.second_player = self.players.get_second_player()
        self.second_player_name = self.players.get_second_player_name()
        self.get_second_player_type = PlayerType()
        self.get_second_player_type.set_player_type("Second")
        self.second_player_type = self.get_second_player_type.player_type
        self.get_user_info = PlayerType()
        self.gameboard = Board()
        self.board = self.gameboard.new_board()
        self.moves = Moves()
        self.human = Human()
        self.bot = Bot()
        self.gameboard.full = False
        first_player_vars = [self.first_player, self.first_player_type, self.first_player_name]
        second_player_vars = [self.second_player, self.second_player_type, self.second_player_name]
        self.player_vars = [first_player_vars, second_player_vars]
        self.game_file = "./data/games.csv"
        self.moves_file = "./data/moves.csv"
        self.data_handling = DataHandling(self.game_file, self.moves_file)
        self.dataviz = DataViz(self.data_handling.game_data)
        self.move_num = 1
        
    def gameplay(self):
        self.moves.winner = self.moves.check_for_win(self.board)
        self.gameboard.full = self.gameboard.board_full(self.board)
        while self.moves.winner == False and self.gameboard.full == False:
            self.gameboard.print_board()
            # Return current player type:
            self.current_player_type = self.get_user_info.get_player_type(self.current_player, self.player_vars)
            self.current_player_name = self.get_user_info.get_player_name(self.current_player, self.player_vars)
            print(f"It is {self.current_player}'s turn.")
            if self.current_player_type == 'Human':
                self.move_tup = self.human.play_move(self.board, self.current_player)
            elif self.current_player_type == 'Bot':
                self.move_tup = self.bot.play_move(self.board, self.current_player)
            else:
                print('There is an error with human v. bot play logic')
            self.data_handling.record_move_data(self.move_num, self.current_player_name, self.current_player_type, self.current_player, self.move_tup)
            self.move_num = self.move_num + 1
            # self.move_data_prep = self.data_handling.record_move_data(self.move_data, 1, self.current_player_name, self.current_player_type, self.current_player, self.human.move)
            # self.move_data_prep.to_csv(self.moves_file)
            self.moves.winner = self.moves.check_for_win(self.board)
            if self.moves.winner == True:
                break
            self.gameboard.full = self.gameboard.board_full(self.board)
            if self.gameboard.full == True:
                break
            self.current_player = self.moves.advance_turn(self.current_player)
        if self.moves.winner == True:
            self.gameboard.print_board()
            print(f"{self.current_player} won the game!")
        elif self.gameboard.full == True:
            self.gameboard.print_board()
            print("The game resulted in a draw.")
        self.data_handling.record_game_data(self.moves.winner, self.first_player_name, self.first_player, self.first_player_type, self.second_player_name, self.second_player, self.second_player_type, self.current_player, self.move_num - 1)
        print("\nMove Count:")
        print(f"{self.move_num - 1} moves")
        print("\nLeaderboard:")
        print(self.dataviz.wins_by_player())
        print("\nAverage Moves to Win:")
        print(self.dataviz.move_count_avg())
        self.dataviz.wins_by_type()
        


rungame = RunGame()
rungame.gameplay()