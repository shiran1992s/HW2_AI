"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed
import time
import utils
import SearchAlgos


#TODO: Check if need instance of player and handle fruits
class GameState:
    player = None
    game_board = None
    location = None
    rival_location = None
    fruits_location = dict()

    def __init__(self, game_board, location, rival_location, player):
        self.player = player
        self.game_board = game_board
        self.location = location
        self.rival_location = rival_location
        for row_index, row_value in enumerate(game_board): #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
            for cell_index, cell_value in enumerate(row_value):
                if cell_value > 2:
                    location = (row_index, cell_index)
                    self.fruits_location.update({location: cell_value})

    def make_move(self, move, maximizing_player):
        if maximizing_player:
            self.game_board[self.location[0]][self.location[1]] = -1
            self.location = (self.location[0] + move[0], self.location[1] + move[1])
            cell_value = self.game_board[self.location[0]][self.location[1]]
            self.player.eat_fruit(cell_value, self.location)
            self.game_board[self.location[0]][self.location[1]] = 1
        else:
            self.game_board[self.rival_location[0]][self.rival_location[1]] = -1
            self.rival_location = (self.rival_location[0] + move[0], self.rival_location[1] + move[1])
            cell_value = self.game_board[self.rival_location[0]][self.rival_location[1]]
            self.player.eat_fruit(cell_value, self.rival_location)
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2

    def undo_move(self, move, maximizing_player):
        if maximizing_player:
            self.game_board[self.location[0]][self.location[1]] = 0
            self.location = (self.location[0] - move[0], self.location[1] - move[1])
            cell_value = self.game_board[self.location[0]][self.location[1]]
            self.player.eat_fruit(cell_value, self.location)
            self.game_board[self.location[0]][self.location[1]] = 1
        else:
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 0
            self.rival_location = (self.rival_location[0] - move[0], self.rival_location[1] - move[1])
            cell_value = self.game_board[self.rival_location[0]][self.rival_location[1]]
            self.player.eat_fruit(cell_value, self.rival_location)
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.penalty_score = penalty_score
        self.location = None
        self.game_board = None
        self.rival_location = None
        self.rival_points = 0
        self.points = 0
        self.time_ended = False
        self.start_time = 0
        self.fruit_locations = dict()
        self.fruit_locations_life_time = dict() #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
        self.best_fruit_value = 0
        self.best_fruit_location = None
        self.moves_available = []
        self.moves_available_count = 0
        self.rival_moves_available = []
        self.rival_moves_available_count = 0
        self.min_dimention = None #TODO: IF NOT USED REMOVE ITS FOR FRUITS_LIFE_TIME
        self.fruits_concentration = None
        self.init_concentration_dict()
        self.directions = [(1,0), (0,1), (-1,0), (0,-1)]

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.

        # TODO: Check if need to update the fruit locations in here or only players.
        self.game_board = board
        self.init_concentration_dict()
        number_of_rows = len(board)
        number_of_cols = len(board[0])
        self.min_dimention = number_of_rows if number_of_rows <= number_of_cols else number_of_cols
        # number_of_players = 2
        for row_index, row_value in enumerate(board):
            for cell_index, cell_value in enumerate(row_value):
                if cell_value == 1:
                    self.location = (row_index, cell_index)
                    # number_of_players -= 1
                if cell_value == 2:
                    self.rival_location = (row_index, cell_index)
                    # number_of_players -= 1
                # if number_of_players is 0:
                #     break
                if cell_value > 2:
                    location = (row_index, cell_index)
                    self.fruit_locations.update({location: cell_value})
                    self.update_fruits_concentration(location)
                    self.fruit_locations_life_time.update({location: self.min_dimention}) #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
                    if cell_value > self.best_fruit_value:
                        self.best_fruit_value = cell_value
                        self.best_fruit_location = (row_index, cell_index)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #TODO: erase the following line and implement this function.
        start_time = time.time()
        num_of_rows = len(self.game_board)
        num_of_cols = len(self.game_board[0])
        board_size = num_of_rows * num_of_cols
        depth = 0
        max_score_move = None
        max_score = -np.inf
        self.game_board[self.location] = -1

        while True: # Do while
            start_it_time = time.time()
            depth += 1

            for d in self.directions:
                row = self.location[0] + d[0]
                col = self.location[1] + d[1]
                if 0 <= row < num_of_rows and 0 <= col < num_of_cols and \
                        self.game_board[row][col] != -1 and self.game_board[row][col] != 2:
                    loc = (row, col)
                    temp_state = GameState(self.game_board,self.location,self.rival_location,self.fruit_locations)
                    score = SearchAlgos.MiniMax.search(self, temp_state, depth, ?player?) #?????
                    if score > max_score:
                        if max_score != -np.inf:
                            self.game_board[self.location + max_score_move] = loc_score
                        max_score = score
                        max_score_move = d
                        loc_score = self.game_board[self.location + max_score_move]
                        self.game_board[self.location + max_score_move] = 1

            it_time = time.time() - start_it_time
            if depth == 1:
                first_it_time = it_time
            next_it_time = first_it_time + 4 * it_time #Im not sure that this is the right calculation (5)
            total_time = time.time() - start_time
            if total_time + next_it_time >= time_limit or depth > board_size/2:
                break


        if max_score_move is None:
            exit()

        return max_score_move












    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        #TODO: erase the following line and implement this function.
        self.game_board[self.rival_location[0]][self.rival_location[1]] = -1
        cell_value = self.game_board[pos[0]][pos[1]]
        if cell_value > 2:
            self.rival_points += cell_value
            self.fruit_locations.pop(pos)
            if pos == self.best_fruit_location:
                self.find_best_fruit()
        self.game_board[pos[0]][pos[1]] = 2
        self.rival_location = pos

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.

        #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
        current_locations = self.fruit_locations
        current_life_time = self.fruit_locations_life_time
        self.fruit_locations_life_time = dict()
        for location, value in fruits_on_board_dict.items():
            if location not in current_locations:
                self.fruit_locations_life_time.update({location: 0})
            else:
                self.fruit_locations_life_time.update({location: current_life_time.get(location) - 1})

        self.fruit_locations = fruits_on_board_dict

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    # calculate manhattan distance
    def manhattan_distance(self, first_location, second_location):
        return sum(abs(e1 - e2) for e1, e2 in zip(first_location, second_location))

    def state_score(self, board, pos):
        num_steps_available = 0
        for d in self.directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]

            # check legal move
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
                num_steps_available += 1

        if num_steps_available == 0:
            return -1
        else:
            return 4 - num_steps_available

    def init_concentration_dict(self):

        self.fruits_concentration = {"first_quarter": 0,
                                     "second_quarter": 0,
                                     "third_quarter": 0,
                                     "forth_quarter": 0}

    def update_fruits_concentration(self, location):
        row_index, col_index = location[0], location[1]
        max_row_index = len(self.game_board) - 1
        max_col_index = len(self.game_board[0]) - 1
        if row_index <= max_row_index/2 and col_index <= max_col_index/2:
            self.fruits_concentration.update({"forth_quarter": self.fruits_concentration.get("forth_quarter") + 1})
        elif row_index >= max_row_index / 2 and col_index <= max_col_index / 2:
            self.fruits_concentration.update({"second_quarter": self.fruits_concentration.get("second_quarter") + 1})
        elif row_index >= max_row_index / 2 and col_index >= max_col_index / 2:
            self.fruits_concentration.update({"first_quarter": self.fruits_concentration.get("first_quarter") + 1})
        elif row_index <= max_row_index / 2 and col_index >= max_col_index / 2:
            self.fruits_concentration.update({"third_quarter": self.fruits_concentration.get("third_quarter") + 1})

    def number_of_legal_cells_from_location(self, location):
        steps_number = 0
        for d in self.directions:
            i = location[0] + d[0]
            j = location[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] not in [-1, 1, 2]:
                steps_number += 1
        return steps_number

    def board_handler(self, state):
        self.init_concentration_dict()
        total_free_cells, total_fruits, fruits_locations_value = 0, 0, dict()
        for row_index, row_value in enumerate(state.game_board):
            for cell_index, cell_value in enumerate(row_value):
                if cell_value == 0:
                    total_free_cells += 1
                if cell_value > 2:
                    location = (row_index, cell_index)
                    total_fruits += 1
                    total_free_cells += 1
                    fruits_locations_value.update({location: cell_value})
                    self.update_fruits_concentration(location)

        fruits_concentration = self.fruits_concentration

        player_bestfruit_manhattan_dist = self.manhattan_distance(state.location, state.player.best_fruit_location)
        rival_bestfruit_manhattan_dist = self.manhattan_distance(state.rival_location, state.player.best_fruit_location)


        # player_row_location, player_col_location,\
        # rival_row_location, rival_col_location = state.location[0], state.location[1],\
        #                                          state.rival_location[0], state.rival_location[1]

        return total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist,\
               rival_bestfruit_manhattan_dist

    def heuristic(self, state):
        ''' Calculating the player's and the rival's moves locations and count '''
        self_moves_tuple, rival_moves_tuple = self.available_moves_handler(state.location, state.rival_location)
        player_moves, player_moves_number = self_moves_tuple[0], self_moves_tuple[1]
        rival_moves, rival_moves_number = rival_moves_tuple[0], rival_moves_tuple[1]

        ''' Calculating board parameters
            1) Total number of available cells
            2) Dictionary of fruit location -> fruit value
            3) Fruits concentration on the board
            4) Manhattan distance between player and the fruit with the highest value
            5) Manhattan distance between rival and the fruit with the highest value
            '''
        total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist, \
        rival_bestfruit_manhattan_dist = self.board_handler(state)

        ''' Calculating the quarter with the highest concentration'''
        quarter_with_highest_concentration = max(fruits_concentration, key=fruits_concentration.get)

        ''' Calculating the moves that will block some of the rival moves'''
        blocking_moves = [move for move in player_moves if move in rival_moves]

        ''' Calculating the moves that the successor will be able to do'''
        successor_available_moves = [move for move in player_moves if self.number_of_legal_cells_from_location(move) > 1]

        ''' Calculating the location score like in simple player'''
        player_location_score = self.state_score(board=self.board, pos=state.location)
        rival_location_score = self.state_score(board=self.board, pos=state.rival_location)

        ''' Calculating the board size'''
        board_size = len(self.board) * len(self.board[0])


    def find_best_fruit(self):
        best_location = max(self.fruit_locations, key=self.fruit_locations.get)
        best_value = self.fruit_locations[best_location]

        if best_value >= self.best_fruit_value:
            self.best_fruit_value = best_value
            self.best_fruit_location = best_location

    def eat_fruit(self, cell_value, position):
        if cell_value > 2:
            self.fruit_locations.pop(position)
            self.fruit_locations_life_time.pop(position) #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
            if cell_value == self.best_fruit_value:
                self.find_best_fruit()

    def check_time(self):
        return time.time() - self.start_time > self.time_limit - 0.01

    ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm

    def available_moves_handler(self, location, rival_location):
        board = self.board
        available_moves, rival_available_moves = [], []
        available_moves_count, rival_available_moves_count = 0, 0

        directions = utils.get_directions()
        for d in directions:
            self_i = location[0] + d[0]
            self_j = location[1] + d[1]
            rival_i = rival_location[0] + d[0]
            rival_j = rival_location[1] + d[1]
            if 0 <= self_i < len(board) and 0 <= self_j < len(board[0]) and board[self_i][self_j] not in [-1, 1, 2]:
                available_moves.append((self_i, self_j))
                available_moves_count += 1
            if 0 <= rival_i < len(board) and 0 <= rival_j < len(board[0]) and board[rival_i][rival_j] not in [-1, 1, 2]:
                rival_available_moves.append((rival_i, rival_j))
                rival_available_moves_count += 1

        self_moves_tuple = (available_moves, available_moves_count)
        rival_moves_tuple = (rival_available_moves, rival_available_moves_count)

        return self_moves_tuple, rival_moves_tuple


#TODO: very basic need to consider fruits positions and values
    def utility(self, current_state):

        self_moves_tuple, rival_moves_tuple = self.available_moves_handler(current_state.location,
                                                                           current_state.rival_location)

        if self_moves_tuple[1] is 0 and self.rival_moves_tuple[1] is 0:
            return 0
        if self.self_moves_tuple[1] >= 1:
            return 1
        return -1

