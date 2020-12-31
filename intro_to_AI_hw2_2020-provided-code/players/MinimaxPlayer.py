"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed
import time
import utils
import SearchAlgos


#TODO: Check if need instance of player and handle fruits

class FruitsState:
    fruit_locations = None
    best_fruit_value = None
    best_fruit_location = None
    fruits_concentration = None

    def __init__(self, fruit_locations, best_fruit_value, best_fruit_location, fruits_concentration):
        self.fruit_locations = fruit_locations
        self.best_fruit_value = best_fruit_value
        self.best_fruit_location = best_fruit_location
        self.fruits_concentration = fruits_concentration


class GameState:
    player = None
    game_board = None
    location = None
    rival_location = None
    last_cell_value_player = []
    last_cell_value_rival = []
    fruit_locations = None
    fruit_life_time = None
    best_fruit_value = None
    best_fruit_location = None
    fruits_in_game = False
    penalty_score = None
    rival_points = None
    points = None
    fruits_concentration = None
    fruits_state = []
    fruits_initial_state = None

    # moves_available = []
    # moves_available_count = 0
    # rival_moves_available = []
    # rival_moves_available_count = 0

    def __init__(self, game_board, location, rival_location, player):
        self.player = player
        self.game_board = game_board
        self.location = location
        self.rival_location = rival_location
        self.fruit_life_time = player.fruit_life_time
        self.penalty_score = player.penalty_score
        self.rival_points = player.rival_points
        self.points = player.points
        if player.fruit_locations is not None and len(player.fruit_locations) > 0:
            self.fruit_locations = dict(player.fruit_locations)
            self.best_fruit_value = player.best_fruit_value
            self.best_fruit_location = tuple(player.best_fruit_location)
            self.fruits_in_game = True
            self.fruits_concentration = dict(player.fruits_concentration)
            self.fruits_initial_state = FruitsState(self.fruit_locations, self.best_fruit_value
                                                    , self.best_fruit_location, self.fruits_concentration)
        # for row_index, row_value in enumerate(game_board): #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
        #     for cell_index, cell_value in enumerate(row_value):
        #         if cell_value > 2:
        #             location = (row_index, cell_index)
        #             self.fruits_location.update({location: cell_value})

    def make_move(self, move, maximizing_player):
        if maximizing_player:
            self.game_board[self.location[0]][self.location[1]] = -1
            self.location = (self.location[0] + move[0], self.location[1] + move[1])
            cell_value = self.game_board[self.location[0]][self.location[1]]
            self.last_cell_value_player.append(cell_value)
            if self.fruit_locations is not None and self.location in self.fruit_locations:
                self.eat_fruit(cell_value, self.location, maximizing_player)
            self.game_board[self.location[0]][self.location[1]] = 1
        else:
            self.game_board[self.rival_location[0]][self.rival_location[1]] = -1
            self.rival_location = (self.rival_location[0] + move[0], self.rival_location[1] + move[1])
            cell_value = self.game_board[self.rival_location[0]][self.rival_location[1]]
            self.last_cell_value_rival.append(cell_value)
            if self.fruit_locations is not None and self.location in self.fruit_locations:
                self.eat_fruit(cell_value, self.rival_location, maximizing_player)
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2

        if self.fruits_in_game:
            # if self.fruit_life_time > 0:
                self.fruit_life_time -= 1
                if self.fruit_life_time == 0:
                    self.fruits_state.append(FruitsState(self.fruit_locations, self.best_fruit_value
                                                         , self.best_fruit_location, self.fruits_concentration))
                    self.update_fruits(self.fruit_locations)

    def undo_move(self, move, maximizing_player):
        if maximizing_player:
            cell_value = self.last_cell_value_player.pop()
            self.game_board[self.location[0]][self.location[1]] = cell_value
            if self.fruit_locations is not None and self.location in self.player.fruit_locations:
                self.cancel_eat_fruit(cell_value, self.location, maximizing_player)
            # self.game_board[self.location[0]][self.location[1]] = 0
            self.location = (self.location[0] - move[0], self.location[1] - move[1])
            self.game_board[self.location[0]][self.location[1]] = 1

        else:
            cell_value = self.last_cell_value_rival.pop()
            self.game_board[self.rival_location[0]][self.rival_location[1]] = cell_value
            if self.fruit_locations is not None and self.location in self.player.fruit_locations:
                self.cancel_eat_fruit(cell_value, self.rival_location, maximizing_player)
            # self.game_board[self.rival_location[0]][self.rival_location[1]] = 0
            self.rival_location = (self.rival_location[0] - move[0], self.rival_location[1] - move[1])
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2

        if self.fruits_in_game:
            if self.fruit_life_time == 0:
                self.fruit_life_time += 1
                if self.fruits_state is not None and len(self.fruits_state) > 0:
                    self.restore_fruits(self.fruits_state.pop())
            # elif self.fruit_life_time > 0:
            else:
                self.fruit_life_time += 1

    def eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            self.fruit_locations.pop(position)
            update_fruits_concentration(self, position, "MINUS")
            if cell_value == self.best_fruit_value:
                find_best_fruit(self)
            if maximizing_player:
                self.points += cell_value
            else:
                self.rival_points += cell_value


    def cancel_eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            self.fruit_locations.update({position: cell_value})
            update_fruits_concentration(self, position, "PLUS")
            if cell_value > self.best_fruit_value:
                find_best_fruit(self)
            if maximizing_player:
                self.points -= cell_value
            else:
                self.rival_points -= cell_value

    def update_fruits(self, fruits_on_board_dict):

        if fruits_on_board_dict is not None and len(fruits_on_board_dict) > 0:
            fruit_positions = fruits_on_board_dict.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] > 2:
                    self.game_board[pos[0], pos[1]] = 0

            self.fruit_locations = None
            self.best_fruit_location = None
            self.best_fruit_value = None

    def restore_fruits(self, fruit_state):
        if fruit_state is not None:
            self.fruit_locations = fruit_state.fruit_locations
            self.best_fruit_location = fruit_state.best_fruit_location
            self.best_fruit_value = fruit_state.best_fruit_value
            self.fruits_concentration = fruit_state.fruits_concentration

        if self.fruit_locations is not None and len(self.fruit_locations) > 0:
            fruit_positions = self.fruit_locations.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] == 0:
                    self.game_board[pos[0], pos[1]] = self.fruit_locations[pos]


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
        self.fruits_in_game = False
        self.best_fruit_location = None
        self.moves_available = []
        self.moves_available_count = 0
        self.rival_moves_available = []
        self.rival_moves_available_count = 0
        self.min_dimention = None
        self.fruits_concentration = None
        # self.init_concentration_dict()
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
        init_concentration_dict(self)
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
                    self.fruits_in_game = True
                    location = (row_index, cell_index)
                    self.fruit_locations.update({location: cell_value})
                    update_fruits_concentration(self, location, "PLUS")
                    # self.fruit_life_time.update({location: self.min_dimention}) #TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
                    if cell_value > self.best_fruit_value:
                        self.best_fruit_value = cell_value
                        self.best_fruit_location = (row_index, cell_index)
                if self.fruits_in_game:
                    self.fruit_life_time = self.min_dimention * 2
                else:
                    self.fruit_life_time = 0


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
        best_move_chosen = available_moves[0]
        depth_limit_from_current_state = get_free_cells_num(current_game_state)

        begin_update_time = time.time()
        self.location = current_game_state.location
        end_update_time = time.time()
        total_update_time = end_update_time - begin_update_time

        while True:  # Do while
            result_values = dict()
            start_it_time = time.time()
            depth += 1
            if depth > depth_limit_from_current_state:
                break
            # if depth != 1:
            #     current_game_state.undo_move(move, True)
            # print(f'In Depth = {depth} ,maximizing_player={True}, available_moves:{available_moves}\n\n\n')
            for move in available_moves:
                if move is None:
                    exit()
                # print(f'In Depth = {depth} ,maximizing_player={True}, player making move:{move}\n')
                current_game_state.make_move(move, True)
                move_minimax_value, move_2 = self.search_algos.search(current_game_state, depth, False)

                result_values.update({move: move_minimax_value})
                current_game_state.undo_move(move, True)
                # print(f'In Depth = {depth} ,maximizing_player={True}, player undoing move:{move}\n')

            it_time = time.time() - start_it_time
            if depth == 1:
                first_it_time = it_time
            next_it_time = first_it_time + 4 * it_time  # Im not sure that this is the right calculation (5)
            total_time = time.time() - start_time
            # if depth >= board_size / 2:
            #     break
            # if depth == 8:
            #     break
            if total_time + next_it_time + total_update_time >= time_limit or depth > board_size:
                break
            best_move_chosen = max(result_values, key=result_values.get)
            # print(f'\n\n\nIn Depth = {depth} ,maximizing_player={True},\n'
            #       f'minmaxValue:{result_values} and the best move chosen is:{best_move_chosen}\n\n\n')

        current_game_state.make_move(best_move_chosen, True)
        sync_objects(self, current_game_state)
        # if self.fruits_in_game:
        #     if self.fruit_life_time > 0:
        #         self.fruit_life_time -= 1
        #         if self.fruit_life_time == 0:
        #             self.fruits_life_ended(self.fruit_locations)
        return best_move_chosen

    # def make_move(self, time_limit, players_score):
    #     """Make move with this Player.
    #     input:
    #         - time_limit: float, time limit for a single turn.
    #     output:
    #         - direction: tuple, specifing the Player's movement, chosen from self.directions
    #     """
    #     # TODO: erase the following line and implement this function.
    #     start_time = time.time()
    #     num_of_rows = len(self.game_board)
    #     num_of_cols = len(self.game_board[0])
    #     board_size = num_of_rows * num_of_cols
    #     depth = 0
    #     current_game_state = GameState(self.game_board, self.location, self.rival_location, self)
    #     available_moves = get_moves_from_location(current_game_state, True)
    #     move = None
    #     # depth_limit_from_current_state = self.(self.)
    #
    #     begin_update_time = time.time()
    #     self.location = current_game_state.location
    #     end_update_time = time.time()
    #     total_update_time = end_update_time - begin_update_time
    #
    #     while True:  # Do while
    #         # result_values = []
    #         start_it_time = time.time()
    #         depth += 1
    #         if depth != 1:
    #             current_game_state.undo_move(move, True)
    #
    #         move_minimax_value, move = self.search_algos.search(current_game_state, depth, True)
    #         if move is None:
    #             exit()
    #         current_game_state.make_move(move, True)
    #
    #         it_time = time.time() - start_it_time
    #         if depth == 1:
    #             first_it_time = it_time
    #         next_it_time = first_it_time + 4 * it_time  # Im not sure that this is the right calculation (5)
    #         total_time = time.time() - start_time
    #         # if depth > 4:
    #         #     break
    #         if total_time + next_it_time + total_update_time >= time_limit or depth == board_size:
    #             break

        # self.location = current_game_state.location
        # if self.fruit_life_time > 0:
        #     self.fruit_life_time -= 1
        #     if self.fruit_life_time == 0:
        #         self.update_fruits(self.fruit_locations)
        # return move

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
            if self.fruit_life_time > 0:
                self.rival_points += cell_value
                print("pos= (", pos[0], ",", pos[1], ")") # TODO: remove!!
                self.fruit_locations.pop(pos)
                update_fruits_concentration(self, pos, "MINUS")
                if pos == self.best_fruit_location:
                    find_best_fruit(self)
        self.game_board[pos[0]][pos[1]] = 2
        self.rival_location = pos
        if self.fruits_in_game:
            self.fruit_life_time -= 1

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.

        # if fruits_on_board_dict is not None:
        #     fruit_positions = fruits_on_board_dict.keys()
        #     for pos in fruit_positions:
        #         if self.game_board[pos[0], pos[1]] > 2:
        #             self.game_board[pos[0], pos[1]] = 0
        #     self.fruit_locations = None
        #     self.best_fruit_location = None
        #     self.best_fruit_value = None

        self.fruit_locations = dict(fruits_on_board_dict)

    def fruits_life_ended(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.

        if fruits_on_board_dict is not None and len(fruits_on_board_dict) > 0:
            fruit_positions = fruits_on_board_dict.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] > 2:
                    self.game_board[pos[0], pos[1]] = 0
            self.fruit_locations = None
            self.best_fruit_location = None
            self.best_fruit_value = None

        # self.fruit_locations = dict(fruits_on_board_dict)

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

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

    # def check_time(self):
    #     return time.time() - self.start_time > self.time_limit - 0.01

# TODO: very basic need to consider fruits positions and values

    def utility(self, current_state):
        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                      current_state.rival_location)
        if self_moves_tuple[1] == 0 or rival_moves_tuple[1] == 0:
            if self_moves_tuple[1] > 0:
                if current_state.points > current_state.rival_points - current_state.penalty_score:
                    return float("inf")
                elif current_state.points < current_state.rival_points - current_state.penalty_score:
                    return float("-inf")
                else:
                    return 0
            elif rival_moves_tuple[1] > 0:
                if current_state.points - current_state.penalty_score > current_state.rival_points:
                    return float("inf")
                elif current_state.points - current_state.penalty_score < current_state.rival_points:
                    return float("-inf")
                else:
                    return 0
        return 0

    def is_goal(self, current_state):
        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                           current_state.rival_location)
        if self_moves_tuple[1] == 0 or rival_moves_tuple[1] == 0:
            return True
        return False

 ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm


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


def get_free_cells_num(state):
    free_cells = 0
    for row_index, row_value in enumerate(state.game_board):
        for cell_index, cell_value in enumerate(row_value):
            if cell_value == 0:
                free_cells += 1
    return free_cells


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
    total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist\
    , rival_bestfruit_manhattan_dist, fruits_locations = board_handler(state)

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
    player_quarter = location_in_quarter(state, state.location)
    rival_quarter = location_in_quarter(state, state.rival_location)

    player_quarter_is_best = player_quarter == quarter_with_highest_concentration
    rival_quarter_is_best = rival_quarter == quarter_with_highest_concentration
    ''' Calculating the moves that the successor will be able to do'''
    successor_available_moves = [move for move in player_moves if number_of_legal_cells_from_location(state, move) >= 1]

    ''' Calculating the Manhattan distance between successor available moves and the fruit with the highest value'''
    succs_moves_manhattan_dists = get_manhattan_dists_for_succ(successor_available_moves, state)
    moves_avg_value = 0
    if len(succs_moves_manhattan_dists) > 0:
        moves_avg_value = sum(succs_moves_manhattan_dists.values())/len(succs_moves_manhattan_dists)

    ''' Calculating the board size'''
    board_size = len(state.game_board) * len(state.game_board[0])
    middle_of_board = [int(len(state.game_board)/2), int(len(state.game_board[0])/2)]
    ''' Calculating Manhattan distance between player position and the fruits positions '''

    """new"""

    points_per_d = 0
    rival_points_per_d = 0
    loc_in_board = 0
    if state.fruits_in_game and state.fruit_life_time > 0:
        for fruit_loc in fruits_locations:
            if manhattan_distance(state.location, fruit_loc) <= state.fruit_life_time:
                points_per_d += fruits_locations_value[fruit_loc] / manhattan_distance(state.location, fruit_loc)
            if manhattan_distance(state.rival_location, fruit_loc) <= state.fruit_life_time:
                rival_points_per_d += fruits_locations_value[fruit_loc] / manhattan_distance(state.rival_location, fruit_loc)
    else:
        close_to_mid = manhattan_distance(state.location, middle_of_board)
        close_to_rival = manhattan_distance(state.location, state.rival_location)
        rival_close_mid = manhattan_distance(state.rival_location, middle_of_board)
        loc_in_board = 4/(close_to_mid + 1) - 1/(rival_close_mid + 1) + 2/(close_to_rival)
    penalty = 0
    if rival_moves_number == 0:
        penalty = state.penalty_score
    if player_moves_number == 0:
        penalty -= state.penalty_score


    """."""

    # points_per_dist = 0
    # if state.fruits_in_game:
    #     if state.fruit_life_time > 0:
    #         temp_points_per_dist_list = []
    #         temp_add_points = 0
    #         for move in player_moves:
    #             temp_points_per_dist_list = [state.game_board[fruit_location[0]][fruit_location[1]] / manhattan_distance(move, fruit_location) #TODO: be shure that the distance from move to fruit is not 0
    #                                          for fruit_location in state.fruit_locations
    #                                          if manhattan_distance(move, fruit_location) <= (state.fruit_life_time / 2) and manhattan_distance(move, fruit_location) > 0]

    #             # for fruits_loc in state.fruit_locations:
    #             #     if manhattan_distance(move, fruits_loc) == 0:
    #             #         temp_add_points += state.game_board[fruit_loc[0]][fruit_loc[1]]
    #             #     elif manhattan_distance(move, fruits_loc) <= (state.fruit_life_time / 2):
    #             #         points_per_dist += state.game_board[fruit_loc[0]][fruit_loc[1]] / manhattan_distance(move, fruit_location)

    #         if temp_points_per_dist_list is not None and len(temp_points_per_dist_list) > 0:
    #             points_per_dist = sum(temp_points_per_dist_list)

    # rival_points_per_dist = 0
    # if state.fruits_in_game:
    #     if state.fruit_life_time > 0:
    #         for move in rival_moves:
    #             temp_rival_points_per_dist_list = [state.game_board[fruit_location[0]][fruit_location[1]] / manhattan_distance(move, fruit_location) #TODO: be shure that the distance from move to fruit is not 0
    #                                          for fruit_location in state.fruit_locations
    #                                          if manhattan_distance(move, fruit_location) <= (state.fruit_life_time / 2) and manhattan_distance(move, fruit_location) > 0]
    #         if temp_rival_points_per_dist_list is not None and len(temp_rival_points_per_dist_list) > 0:
    #             rival_points_per_dist = sum(temp_rival_points_per_dist_list)
    """end new"""

    avg_distances = 0
    succ_avg_distances = 0
    if state.fruits_in_game:
        if state.fruit_life_time > 0:
            player_distances_from_fruits = dict()
            for move in player_moves:
                # TODO: change the avg to weighted avg by the value of each fruit
                 temp_distances_list = [manhattan_distance(move, fruit_location)
                                        for fruit_location in state.fruit_locations
                                        if manhattan_distance(move, fruit_location) <= state.fruit_life_time / 2]
            if temp_distances_list is not None and len(temp_distances_list) > 0:
                player_distances_from_fruits.update({tuple(temp_distances_list): sum(temp_distances_list)
                                                                              / len(temp_distances_list)})

            if len(player_distances_from_fruits) == 0: #TODO: think how to fix
                avg_distances = 0
            else:
                avg_distances = sum(player_distances_from_fruits.values()) / len(player_distances_from_fruits)

            succ_distances_from_fruits = dict()
            for move in successor_available_moves:
                temp_distances_list = [manhattan_distance(move, fruit_location) for fruit_location in state.fruit_locations
                                       if manhattan_distance(move, fruit_location) <= state.fruit_life_time / 2]
                if temp_distances_list is not None and len(temp_distances_list) > 0:
                    succ_distances_from_fruits.update({tuple(temp_distances_list): sum(temp_distances_list)
                                                                              / len(temp_distances_list)})

            # succ_avg_distances = sum(succ_distances_from_fruits.values()) / len(succ_distances_from_fruits)
            if len(succ_distances_from_fruits) == 0:
                succ_avg_distances = 0
            else:
                succ_avg_distances = sum(succ_distances_from_fruits.values()) / len(succ_distances_from_fruits)

    ''' Calculating the location score like in simple player'''
    player_location_score = state.player.state_score(board=state.game_board, pos=state.location)
    rival_location_score = state.player.state_score(board=state.game_board, pos=state.rival_location)

    value = None
#    if total_free_cells / board_size <= 0.5:
#        if state.fruit_life_time > 0:
#            value = 5 * state.points + 4 * player_moves_with_fruits_points - 3 * avg_distances - 2 * succ_avg_distances

            # value = 3 * player_bestfruit_manhattan_dist - 1 * rival_bestfruit_manhattan_dist \
            #         + (3.5 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (9 * moves_avg_value) \
            #         + (7 * player_moves_with_fruits_points) - (2 * rival_moves_with_fruits_points)
#        else:
            # value = (0.6 * player_moves_number) - (0.9 * rival_moves_number) \
            #         + (len(blocking_moves)) + (0.7 * len(successor_available_moves)) \
            #         + 2 * player_bestfruit_manhattan_dist - 1.1 * rival_bestfruit_manhattan_dist \
            #         + (3 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (2 * moves_avg_value) \
            #         + (3 * player_moves_with_fruits_points) - (1.5 * rival_moves_with_fruits_points) \
            #         + player_location_score - rival_location_score

            # value = 3 * player_bestfruit_manhattan_dist - 1 * rival_bestfruit_manhattan_dist \
            #         + (3.5 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (9 * moves_avg_value) \
            #         + (7 * player_moves_with_fruits_points) - (2 * rival_moves_with_fruits_points)

            # value = 5 * state.points + 4 * player_moves_with_fruits_points - avg_distances * 3 - succ_avg_distances * 2
#            value = 5 * state.points

#    else:
#        if state.fruit_life_time > 0:
#            value = 7 * state.points + 5 * player_moves_with_fruits_points - avg_distances * 5 - succ_avg_distances * 3

            # value = 3 * player_bestfruit_manhattan_dist - 1 * rival_bestfruit_manhattan_dist \
            #         + (3.5 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (12 * moves_avg_value) \
            #         + (9 * player_moves_with_fruits_points) - (2 * rival_moves_with_fruits_points)
#        else:
            # value = (0.6 * player_moves_number) - (0.9 * rival_moves_number) \
            #         + (len(blocking_moves)) + (0.7 * len(successor_available_moves)) \
            #         + 2 * player_bestfruit_manhattan_dist - 1.1 * rival_bestfruit_manhattan_dist \
            #         + (3 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (2 * moves_avg_value) \
            #         + (3 * player_moves_with_fruits_points) - (1.5 * rival_moves_with_fruits_points) \
            #         + player_location_score - rival_location_score

            # value = 7 * state.points + 5 * player_moves_with_fruits_points - avg_distances * 5 - succ_avg_distances * 3
#            value = 7 * state.points

            # value = 3 * player_bestfruit_manhattan_dist - 1 * rival_bestfruit_manhattan_dist \
            #         + (3.5 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (12 * moves_avg_value) \
            #         + (9 * player_moves_with_fruits_points) - (2 * rival_moves_with_fruits_points)

    value = 8 * state.points + 2 * points_per_d - 4 * state.rival_points - rival_points_per_d + 0.25 * loc_in_board + 8 * penalty
    return value


def get_manhattan_dists_for_succ(succ_moves, state):
    dists = dict()
    for move in succ_moves:
        manhattan_val = manhattan_distance(move, state.player.best_fruit_location)
        dists.update({move: manhattan_val})

    return dists


def find_best_fruit(object):
    if object.fruit_locations is not None and len(object.fruit_locations) > 0:
        best_location = max(object.fruit_locations, key=object.fruit_locations.get)
        best_value = object.fruit_locations[best_location]

        if best_value >= object.best_fruit_value:
            object.best_fruit_value = best_value
            object.best_fruit_location = best_location


def board_handler(object_input):
    init_concentration_dict(object_input)
    total_free_cells, total_fruits, fruits_locations_value = 0, 0, dict()
    fruits_locations = []
    for row_index, row_value in enumerate(object_input.game_board):
        for cell_index, cell_value in enumerate(row_value):
            if cell_value == 0:
                total_free_cells += 1
            if cell_value > 2:
                location = (row_index, cell_index)
                total_fruits += 1
                total_free_cells += 1
                fruits_locations.append(location)
                fruits_locations_value.update({location: cell_value})
                update_fruits_concentration(object_input, location, "PLUS")

    fruits_concentration = object_input.fruits_concentration

    if object_input.best_fruit_location is not None:
        player_bestfruit_manhattan_dist = manhattan_distance(object_input.location,
                                                                  object_input.best_fruit_location)
        rival_bestfruit_manhattan_dist = manhattan_distance(object_input.rival_location,
                                                                 object_input.best_fruit_location)
    else:
        player_bestfruit_manhattan_dist = 0
        rival_bestfruit_manhattan_dist = 0

    # player_row_location, player_col_location,\
    # rival_row_location, rival_col_location = state.location[0], state.location[1],\
    #                                          state.rival_location[0], state.rival_location[1]

    return total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist, \
           rival_bestfruit_manhattan_dist, fruits_locations


def init_concentration_dict(object_input):
    object_input.fruits_concentration = {"first_quarter": 0,
                                 "second_quarter": 0,
                                 "third_quarter": 0,
                                 "forth_quarter": 0}


def update_fruits_concentration(object_input, location, action):
    row_index, col_index = location[0], location[1]
    max_row_index = len(object_input.game_board) - 1
    max_col_index = len(object_input.game_board[0]) - 1
    if action == "PLUS":
        if row_index <= max_row_index/2 and col_index <= max_col_index/2:
            object_input.fruits_concentration.update({"forth_quarter": object_input.fruits_concentration.get("forth_quarter") + 1})
        elif row_index >= max_row_index / 2 and col_index <= max_col_index / 2:
            object_input.fruits_concentration.update({"second_quarter": object_input.fruits_concentration.get("second_quarter") + 1})
        elif row_index >= max_row_index / 2 and col_index >= max_col_index / 2:
            object_input.fruits_concentration.update({"first_quarter": object_input.fruits_concentration.get("first_quarter") + 1})
        elif row_index <= max_row_index / 2 and col_index >= max_col_index / 2:
            object_input.fruits_concentration.update({"third_quarter": object_input.fruits_concentration.get("third_quarter") + 1})
    elif action == "MINUS":
        if row_index <= max_row_index/2 and col_index <= max_col_index/2:
            object_input.fruits_concentration.update({"forth_quarter": object_input.fruits_concentration.get("forth_quarter") - 1})
        elif row_index >= max_row_index / 2 and col_index <= max_col_index / 2:
            object_input.fruits_concentration.update({"second_quarter": object_input.fruits_concentration.get("second_quarter") - 1})
        elif row_index >= max_row_index / 2 and col_index >= max_col_index / 2:
            object_input.fruits_concentration.update({"first_quarter": object_input.fruits_concentration.get("first_quarter") - 1})
        elif row_index <= max_row_index / 2 and col_index >= max_col_index / 2:
            object_input.fruits_concentration.update({"third_quarter": object_input.fruits_concentration.get("third_quarter") - 1})


def location_in_quarter(object_input, location):
    row_index, col_index = location[0], location[1]
    max_row_index = len(object_input.game_board) - 1
    max_col_index = len(object_input.game_board[0]) - 1
    if row_index <= max_row_index / 2 and col_index <= max_col_index / 2:
        return 4
    elif row_index >= max_row_index / 2 and col_index <= max_col_index / 2:
        return 2
    elif row_index >= max_row_index / 2 and col_index >= max_col_index / 2:
        return 1
    elif row_index <= max_row_index / 2 and col_index >= max_col_index / 2:
        return 3


def number_of_legal_cells_from_location(object_input, location):
    steps_number = 0
    for d in utils.get_directions():
        i = location[0] + d[0]
        j = location[1] + d[1]
        if 0 <= i < len(object_input.game_board) and 0 <= j < len(object_input.game_board[0]) and object_input.game_board[i][j] not in [-1, 1, 2]:
            steps_number += 1
    return steps_number


# calculate manhattan distance
def manhattan_distance(first_location, second_location):
    if first_location is not None and second_location is not None:
        return abs(first_location[0] - second_location[0]) + abs(first_location[1] - second_location[1])
    return 0


# calculate manhattan distance
def sync_objects(first_object, second_object):
    first_object.location = second_object.location
    first_object.points = second_object.points
    if second_object.fruit_locations is not None and len(second_object.fruit_locations) > 0:
        first_object.fruit_locations = dict(second_object.fruit_locations)
        first_object.best_fruit_value = second_object.best_fruit_value
        first_object.best_fruit_location = tuple(second_object.best_fruit_location)



