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
    last_cell_value_player = None
    last_cell_value_rival = None
    fruits_location = dict()
    fruit_life_time = None

    def __init__(self, game_board, location, rival_location, player):
        self.player = player
        self.game_board = game_board
        self.location = location
        self.rival_location = rival_location
        self.fruit_life_time = player.min_dimention
        self.last_cell_value_player = 1
        self.last_cell_value_rival = 2
        for row_index, row_value in enumerate(game_board): #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
            for cell_index, cell_value in enumerate(row_value):
                if cell_value > 2:
                    location = (row_index, cell_index)
                    self.fruits_location.update({location: cell_value})

    def make_move(self, move, maximizing_player):
        if maximizing_player:
            self.game_board[self.location[0]][self.location[1]] = -1
            self.location = (self.location[0] + move[0], self.location[1] + move[1])
            self.fruit_life_time -= 1
            cell_value = self.game_board[self.location[0]][self.location[1]]
            self.last_cell_value_player = cell_value
            self.player.eat_fruit(cell_value, self.location, maximizing_player)
            self.game_board[self.location[0]][self.location[1]] = 1
        else:
            self.game_board[self.rival_location[0]][self.rival_location[1]] = -1
            self.rival_location = (self.rival_location[0] + move[0], self.rival_location[1] + move[1])
            cell_value = self.game_board[self.rival_location[0]][self.rival_location[1]]
            self.last_cell_value_rival = cell_value
            self.player.eat_fruit(cell_value, self.rival_location, maximizing_player)
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2

    def undo_move(self, move, maximizing_player):
        if maximizing_player:
            self.game_board[self.location[0]][self.location[1]] = self.last_cell_value_player
            self.fruit_life_time += 1
            self.player.cancel_eat_fruit(self.last_cell_value_player, self.location, maximizing_player)
            # self.game_board[self.location[0]][self.location[1]] = 0
            self.location = (self.location[0] - move[0], self.location[1] - move[1])
            self.game_board[self.location[0]][self.location[1]] = 1

        else:
            self.game_board[self.rival_location[0]][self.rival_location[1]] = self.last_cell_value_rival
            self.player.cancel_eat_fruit(self.last_cell_value_rival, self.rival_location, maximizing_player)
            # self.game_board[self.rival_location[0]][self.rival_location[1]] = 0
            self.rival_location = (self.rival_location[0] - move[0], self.rival_location[1] - move[1])
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
        self.fruit_life_time = None
        self.best_fruit_value = 0
        self.best_fruit_location = None
        self.moves_available = []
        self.moves_available_count = 0
        self.rival_moves_available = []
        self.rival_moves_available_count = 0
        self.min_dimention = None
        self.fruits_concentration = None
        self.init_concentration_dict()
        self.search_algos = SearchAlgos.MiniMax(self.utility, None, self.make_move, self.is_goal)


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
        self.fruit_life_time = self.min_dimention * 2
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
                    # self.fruit_life_time.update({location: self.min_dimention}) #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
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
        # TODO: erase the following line and implement this function.
        start_time = time.time()
        num_of_rows = len(self.game_board)
        num_of_cols = len(self.game_board[0])
        board_size = num_of_rows * num_of_cols
        depth = 0
        current_game_state = GameState(self.game_board, self.location, self.rival_location, self)
        available_moves = get_moves_from_location(current_game_state, True)
        move = None
        #depth_limit_from_current_state = self.(self.)


        begin_update_time = time.time()
        self.location = current_game_state.location
        end_update_time = time.time()
        total_update_time = end_update_time - begin_update_time

        while True:  # Do while
            # result_values = []
            start_it_time = time.time()
            depth += 1
            if depth != 1:
                current_game_state.undo_move(move, True)

            move_minimax_value, move = self.search_algos.search(current_game_state, depth, True)
            current_game_state.make_move(move, True)

            it_time = time.time() - start_it_time
            if depth == 1:
                first_it_time = it_time
            next_it_time = first_it_time + 4 * it_time  # Im not sure that this is the right calculation (5)
            total_time = time.time() - start_time
            if total_time + next_it_time + total_update_time >= time_limit or depth > board_size / 2:
                break

        if move is None:
            exit()
        self.location = current_game_state.location
        self.fruit_life_time -= 1
        if self.fruit_life_time == 0:
            self.fruit_locations = None
        return move

    # def make_move(self, time_limit, players_score):
    #     """Make move with this Player.
    #     input:
    #         - time_limit: float, time limit for a single turn.
    #     output:
    #         - direction: tuple, specifing the Player's movement, chosen from self.directions
    #     """
    #     #TODO: erase the following line and implement this function.
    #     start_time = time.time()
    #     num_of_rows = len(self.game_board)
    #     num_of_cols = len(self.game_board[0])
    #     board_size = num_of_rows * num_of_cols
    #     depth = 0
    #
    #     self.game_board[self.location] = -1
    #     move = None
    #     while True: # Do while
    #         start_it_time = time.time()
    #         depth += 1
    #         if depth != 1:
    #             self.game_board[self.location + move] = move_score
    #
    #         t_state = {self.game_board, self.location, self, self.rival_location}
    #         # state: {game_board, location, player, rival_location}
    #         move_minimax_value, move = MiniMax.search(self, t_state, depth, True)
    #         move_score = self.game_board[self.location + move_score]
    #         self.game_board[self.location + move] = 1
    #
    #         it_time = time.time() - start_it_time
    #         if depth == 1:
    #             first_it_time = it_time
    #         next_it_time = first_it_time + 4 * it_time # Im not sure that this is the right calculation (5)
    #         total_time = time.time() - start_time
    #         if total_time + next_it_time >= time_limit or depth > board_size/2:
    #             break
    #
    #
    #     if move is None:
    #         exit()
    #     self.location = self.location + move
    #
    #     return move

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
        # current_locations = self.fruit_locations
        # current_life_time = self.fruit_life_time
        # self.fruit_life_time = dict()
        # for location, value in fruits_on_board_dict.items():
        #     if location not in current_locations:
        #         self.fruit_life_time.update({location: 0})
        #     else:
        #         self.fruit_life_time.update({location: current_life_time.get(location) - 1})

        self.fruit_locations = fruits_on_board_dict

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed



    # calculate manhattan distance
    def manhattan_distance(self, first_location, second_location):
        if first_location is not None and second_location is not None:
            return abs(first_location[0] - second_location[0]) + abs(first_location[1] - second_location[1])
        return 0

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

    def location_in_quarter(self, location):
        row_index, col_index = location[0], location[1]
        max_row_index = len(self.game_board) - 1
        max_col_index = len(self.game_board[0]) - 1
        if row_index <= max_row_index / 2 and col_index <= max_col_index / 2:
            return 4
        elif row_index >= max_row_index / 2 and col_index <= max_col_index / 2:
            return 2
        elif row_index >= max_row_index / 2 and col_index >= max_col_index / 2:
            return 1
        elif row_index <= max_row_index / 2 and col_index >= max_col_index / 2:
            return 3

    def number_of_legal_cells_from_location(self, location):
        steps_number = 0
        for d in self.directions:
            i = location[0] + d[0]
            j = location[1] + d[1]
            if 0 <= i < len(self.game_board) and 0 <= j < len(self.game_board[0]) and self.game_board[i][j] not in [-1, 1, 2]:
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

        if self.best_fruit_location is not None:
            player_bestfruit_manhattan_dist = self.manhattan_distance(state.location, state.player.best_fruit_location)
            rival_bestfruit_manhattan_dist = self.manhattan_distance(state.rival_location, state.player.best_fruit_location)
        else:
            player_bestfruit_manhattan_dist = 0
            rival_bestfruit_manhattan_dist = 0


        # player_row_location, player_col_location,\
        # rival_row_location, rival_col_location = state.location[0], state.location[1],\
        #                                          state.rival_location[0], state.rival_location[1]

        return total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist,\
               rival_bestfruit_manhattan_dist


    def find_best_fruit(self):
        if self.fruit_locations is not None and len(self.fruit_locations) > 0:
            best_location = max(self.fruit_locations, key=self.fruit_locations.get)
            best_value = self.fruit_locations[best_location]

            if best_value >= self.best_fruit_value:
                self.best_fruit_value = best_value
                self.best_fruit_location = best_location

    def eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            self.fruit_locations.pop(position)
            # self.fruit_life_time.pop(position) #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
            if cell_value == self.best_fruit_value:
                self.find_best_fruit()
            if maximizing_player:
                self.points += cell_value
            else:
                self.rival_points += cell_value


    def cancel_eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            self.fruit_locations.update({position: cell_value})
            # self.fruit_life_time.pop(position)  # TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
            if cell_value > self.best_fruit_value:
                self.find_best_fruit()

            if maximizing_player:
                self.points -= cell_value
            else:
                self.rival_points -= cell_value

    # def check_time(self):
    #     return time.time() - self.start_time > self.time_limit - 0.01


#TODO: very basic need to consider fruits positions and values
    def utility(self, current_state):

        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                      current_state.rival_location)
        if self_moves_tuple[1] is 0 or rival_moves_tuple[1] is 0:
            if self_moves_tuple[1] > 0:
                if self.points >= self.rival_points:
                    return 10
                else:
                    return 5
            else:
                if self.points >= self.rival_points:
                    return -10
                else:
                    return -30
        return -1


    def is_goal(self, current_state):
        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                           current_state.rival_location)
        if self_moves_tuple[1] == 0 or rival_moves_tuple[1] == 0:
            return True
        return False

 ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm

def available_moves_handler(state, location, rival_location):
    board = state.game_board
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

def get_moves_from_location(state, maximizing_player):
    current_location = state.location if maximizing_player else state.rival_location
    board = state.game_board
    available_moves = []
    directions = utils.get_directions()
    for d in directions:
        current_i = current_location[0] + d[0]
        current_j = current_location[1] + d[1]

        if 0 <= current_i < len(board) and 0 <= current_j < len(board[0]) and board[current_i][current_j] not in [-1, 1, 2]:
            available_moves.append((d[0], d[1]))

    return available_moves

def heuristic(state):
    ''' Calculating the player's and the rival's moves locations and count '''
    self_moves_tuple, rival_moves_tuple = available_moves_handler(state, state.location, state.rival_location)
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
    rival_bestfruit_manhattan_dist = state.player.board_handler(state)

    ''' Calculating the quarter with the highest concentration'''
    quarter_with_highest_concentration = max(fruits_concentration, key=fruits_concentration.get)

    ''' Calculating the moves that will block some of the rival moves'''
    blocking_moves = [move for move in player_moves if move in rival_moves]

    ''' Calculating the moves that will take fruits'''
    player_moves_with_fruits = [move for move in player_moves if move in fruits_locations_value.keys()]
    rival_moves_with_fruits = [move for move in rival_moves if move in fruits_locations_value.keys()]

    ''' Calculating the total points from moves with fruits'''
    player_moves_with_fruits_points, rival_moves_with_fruits_points = 0, 0
    if len(player_moves_with_fruits) > 0:
        player_moves_with_fruits_points = sum([fruits_locations_value[move] for move in player_moves_with_fruits])\
                                      / len(player_moves_with_fruits)
    if len(rival_moves_with_fruits) > 0:
        rival_moves_with_fruits_points = sum([fruits_locations_value[move] for move in rival_moves_with_fruits])\
                                     / len(rival_moves_with_fruits)


    ''' Calculating the locations of Player and Rival according 
    to the quarter with the highest concentration'''
    player_quarter = state.player.location_in_quarter(state.location)
    rival_quarter = state.player.location_in_quarter(state.rival_location)

    player_quarter_is_best = player_quarter == quarter_with_highest_concentration
    rival_quarter_is_best = rival_quarter == quarter_with_highest_concentration
    ''' Calculating the moves that the successor will be able to do'''
    successor_available_moves = [move for move in player_moves if state.player.number_of_legal_cells_from_location(move) > 1]

    ''' Calculating the Manhattan distance between successor available moves and the fruit with the highest value'''
    succs_moves_manhattan_dists = get_manhattan_dists_for_succ(successor_available_moves, state)
    moves_avg_value = 0
    if len(succs_moves_manhattan_dists) > 0:
        moves_avg_value = sum(succs_moves_manhattan_dists.values())/len(succs_moves_manhattan_dists)
    ''' Calculating the location score like in simple player'''
    player_location_score = state.player.state_score(board=state.game_board, pos=state.location)
    rival_location_score = state.player.state_score(board=state.game_board, pos=state.rival_location)

    ''' Calculating the board size'''
    board_size = len(state.game_board) * len(state.game_board[0])

    value = (1 * player_moves_number) - (0.8 * rival_moves_number) \
            + (len(blocking_moves) / 2) + (1.2 * len(successor_available_moves)) \
            + player_location_score - (1.2 * rival_location_score) \
            + player_bestfruit_manhattan_dist - 1.2 * rival_bestfruit_manhattan_dist \
            + (0.2 * player_quarter_is_best) - (0.4 * rival_quarter_is_best) + (0.3 * moves_avg_value) \
            + (0.4 * player_moves_with_fruits_points) - (0.2 * rival_moves_with_fruits_points)
    return value

def get_manhattan_dists_for_succ(succ_moves, state):
    dists = dict()
    for move in succ_moves:
        manhattan_val = state.player.manhattan_distance(move, state.player.best_fruit_location)
        dists.update({move: manhattan_val})

    return dists
