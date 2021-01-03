"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import time
import utils
import SearchAlgos
import copy

# TODO: Check if need instance of player and handle fruits

class FruitsState:
    fruit_locations = None
    best_fruit_value = None
    best_fruit_location = None
    fruits_concentration = None

    def __init__(self, fruit_locations, best_fruit_value, best_fruit_location, fruits_concentration):
        self.fruit_locations = copy.deepcopy(fruit_locations)
        self.best_fruit_value = copy.deepcopy(best_fruit_value)
        self.best_fruit_location = copy.deepcopy(best_fruit_location)
        self.fruits_concentration = copy.deepcopy(fruits_concentration)


class GameState:
    initial_fruit_locations = dict()
    game_board = None
    location = None
    rival_location = None
    last_cell_value_player = []
    last_cell_value_rival = []
    fruit_locations = dict()
    fruit_life_time = None
    best_fruit_value = float('-inf')
    best_fruit_location = None
    fruits_in_game = False
    penalty_score = None
    rival_points = None
    points = None
    fruits_concentration = None
    fruits_state = []
    fruits_initial_state = None


    def __init__(self, game_board, location, rival_location, fruit_life_time, penalty_score, rival_points, points,
                 fruit_locations, best_fruit_value, best_fruit_location, fruits_concentration, fruits_in_game):
        # self.player = player
        self.game_board = copy.deepcopy(game_board)
        self.location = copy.deepcopy(location)
        self.rival_location = copy.deepcopy(rival_location)
        self.fruit_life_time = copy.deepcopy(fruit_life_time)
        self.penalty_score = copy.deepcopy(penalty_score)
        self.rival_points = copy.deepcopy(rival_points)
        self.points = copy.deepcopy(points)
        if fruits_in_game:
            self.fruits_in_game = True
        if fruit_locations is not None:
            self.fruit_locations = copy.deepcopy(fruit_locations)
            self.initial_fruit_locations = copy.deepcopy(fruit_locations)
            self.best_fruit_value = copy.deepcopy(best_fruit_value)
            self.best_fruit_location = copy.deepcopy(best_fruit_location)
            self.fruits_concentration = copy.deepcopy(fruits_concentration)
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
            if self.fruit_locations is not None and self.rival_location in self.fruit_locations:
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

        if self.fruits_in_game:
            if self.fruit_life_time == 0:
                self.fruit_life_time += 1
                if self.fruits_state is not None and len(self.fruits_state) > 0:
                    self.restore_fruits(self.fruits_state.pop())
            # elif self.fruit_life_time > 0:
            else:
                self.fruit_life_time += 1

        if maximizing_player:
            cell_value = self.last_cell_value_player.pop()
            self.game_board[self.location[0]][self.location[1]] = cell_value
            if self.fruit_locations is not None and self.location in self.initial_fruit_locations:
                self.cancel_eat_fruit(cell_value, self.location, maximizing_player)
            # self.game_board[self.location[0]][self.location[1]] = 0
            self.location = (self.location[0] - move[0], self.location[1] - move[1])
            self.game_board[self.location[0]][self.location[1]] = 1

        else:
            cell_value = self.last_cell_value_rival.pop()
            self.game_board[self.rival_location[0]][self.rival_location[1]] = cell_value
            if self.fruit_locations is not None and self.rival_location in self.initial_fruit_locations:
                self.cancel_eat_fruit(cell_value, self.rival_location, maximizing_player)
            # self.game_board[self.rival_location[0]][self.rival_location[1]] = 0
            self.rival_location = (self.rival_location[0] - move[0], self.rival_location[1] - move[1])
            self.game_board[self.rival_location[0]][self.rival_location[1]] = 2


    def eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            # print(f'before eat fruit:\nposition={position},'
            #       f'points:{self.points},rival_points={self.rival_points},'
            #       f' cell_value={cell_value},fruit_locations={self.fruit_locations}\n\n\n')
            self.fruit_locations.pop(position)
            update_fruits_concentration(self, position, "MINUS")
            if cell_value == self.best_fruit_value:
                find_best_fruit(self)
            if maximizing_player:
                self.points += cell_value
            else:
                self.rival_points += cell_value
            # print(f'after eat fruit:\nposition={position},'
            #       f'points:{self.points},rival_points={self.rival_points},'
            #       f' cell_value={cell_value},fruit_locations={self.fruit_locations}\n\n\n')

    def cancel_eat_fruit(self, cell_value, position, maximizing_player):
        if cell_value > 2:
            # print(f'before cancel eat fruit:\nposition={position},'
            #       f'points:{self.points},rival_points={self.rival_points},'
            #       f' cell_value={cell_value},fruit_locations={self.fruit_locations}\n\n\n')
            self.fruit_locations.update({position: cell_value})
            update_fruits_concentration(self, position, "PLUS")
            if cell_value > self.best_fruit_value:
                find_best_fruit(self)
            if maximizing_player:
                self.points -= cell_value
            else:
                self.rival_points -= cell_value
            # print(f'after cancel eat fruit:\nposition={position},'
            #       f'points:{self.points},rival_points={self.rival_points},'
            #       f' cell_value={cell_value},fruit_locations={self.fruit_locations}\n\n\n')

    def update_fruits(self, fruits_on_board_dict):

        if fruits_on_board_dict is not None: #and len(fruits_on_board_dict) > 0
            # print(f'in update_fruits: fruit_locations={self.fruit_locations}\n\n\n')
            fruit_positions = fruits_on_board_dict.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] > 2:
                    self.game_board[pos[0], pos[1]] = 0
            # print(f'after update_fruits: game_board={self.game_board}\n\n\n')
            self.fruit_locations = dict()
            self.best_fruit_location = None
            self.best_fruit_value = float("-inf")

    def restore_fruits(self, fruit_state):
        if fruit_state is not None:
            # print(f'in restore_fruits: fruit_locations={self.fruit_locations}\n\n\n')
            self.fruit_locations = fruit_state.fruit_locations
            self.best_fruit_location = fruit_state.best_fruit_location
            self.best_fruit_value = fruit_state.best_fruit_value
            self.fruits_concentration = fruit_state.fruits_concentration
            # print(f'after restore_fruits: fruit_locations={self.fruit_locations}\n\n\n')
        if self.fruit_locations is not None and len(self.fruit_locations) > 0:
            fruit_positions = self.fruit_locations.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] == 0:
                    self.game_board[pos[0], pos[1]] = self.fruit_locations[pos]
        # print(f'after restore_fruits: game_board={self.game_board}\n\n\n')


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.penalty_score = penalty_score
        self.name = "HeavyAlphaBeta"
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
        self.search_algos = SearchAlgos.AlphaBeta(self.utility, None, self.make_move, self.is_goal)




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
            # print(f'fruit_life_time={self.fruit_life_time}\n\n')
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
        # raise NotImplementedError
        start_time = time.time()


        num_of_rows = len(self.game_board)
        num_of_cols = len(self.game_board[0])
        board_size = num_of_rows * num_of_cols
        depth = 2
        current_game_state = GameState(self.game_board, self.location, self.rival_location, self.fruit_life_time,
                                       self.penalty_score, self.rival_points, self.points, self.fruit_locations,
                                       self.best_fruit_value, self.best_fruit_location, self.fruits_concentration)
        available_moves = get_moves_from_location(current_game_state, True)
        best_move_chosen = available_moves[0]
        depth_limit_from_current_state = get_free_cells_num(current_game_state)

        result_values = dict()
        start_it_time = time.time()

        # print(f'In Depth = {depth} ,maximizing_player={True}, available_moves:{available_moves}\n\n\n')
        for move in available_moves:
            if move is None:
                exit()
            # print(f'In Depth = {depth} ,maximizing_player={True}, player making move:{move}\n')
            current_game_state.make_move(move, True)
            depth -= 1
            move_minimax_value, move_2 = self.search_algos.search(copy.deepcopy(current_game_state), depth, False)

            result_values.update({move: move_minimax_value})
            current_game_state.undo_move(move, True)
            depth += 1
            # print(f'In Depth = {depth} ,maximizing_player={True}, player undoing move:{move}\n')
        # it_time = time.time() - start_it_time
        # if depth == 1:
        #     first_it_time = it_time
        # next_it_time = first_it_time + 4 * it_time
        # total_time = time.time() - start_time
        best_move_chosen = max(result_values, key=result_values.get)
            # print(f'\n\n\nPlayer = {self.name}, In Depth = {depth} ,maximizing_player={True},\n'
            #       f'minmaxValue:{result_values} and the best move chosen is:{best_move_chosen}\n\n\n')

        # print(f'Player = {self.name},before sync:\nlocation={self.location},'
        #       f'points:{self.points}, fruit_life_time={self.fruit_life_time},fruit_locations={self.fruit_locations}\n\n\n')
        # print(f'Player = {self.name},before making move:\nlocation={current_game_state.location},'
        #       f'points:{current_game_state.points}, fruit_life_time={current_game_state.fruit_life_time},fruit_locations={current_game_state.fruit_locations}\n\n\n')
        current_game_state.make_move(best_move_chosen, True)
        # print(f'Player = {self.name},after making move:\nlocation={current_game_state.location},'
        #       f'points:{current_game_state.points}, fruit_life_time={current_game_state.fruit_life_time},fruit_locations={current_game_state.fruit_locations}\n\n\n')
        sync_objects(self,current_game_state.game_board, current_game_state.location, current_game_state.points, current_game_state.fruit_life_time,
                     current_game_state.fruit_locations, current_game_state.best_fruit_location,
                     current_game_state.best_fruit_value)
        # print(f'Player = {self.name},after sync:\nlocation={self.location},'
        #       f'points:{self.points}, fruit_life_time={self.fruit_life_time},fruit_locations={self.fruit_locations}\n\n\n')
        return best_move_chosen

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        print(f'Player= {self.name} updating rival move\n')
        # raise NotImplementedError
        self.game_board[self.rival_location[0]][self.rival_location[1]] = -1
        cell_value = self.game_board[pos[0]][pos[1]]
        if cell_value > 2:
            if self.fruit_life_time > 0:
                self.rival_points += cell_value
                # print(f'pos=({pos[0]}{pos[1]})\n\
                #                         fruit_life_time = {self.fruit_life_time}\n'
                #       f' fruit_locations={self.fruit_locations}\n')  # TODO: remove!!
                self.fruit_locations.pop(pos)
                # print(f'fruit_life_time = {self.fruit_life_time}\n'
                #       f' fruit_locations={self.fruit_locations}\n')
                update_fruits_concentration(self, pos, "MINUS")
                if pos == self.best_fruit_location:
                    find_best_fruit(self)
        self.game_board[pos[0]][pos[1]] = 2
        self.rival_location = pos
        if self.fruits_in_game:
            self.fruit_life_time -= 1
            if self.fruit_life_time == 0:
                self.fruits_life_ended(self.fruit_locations)
            # print(f'fruit_life_time = {self.fruit_life_time}\n'
            #       f' fruit_locations={self.fruit_locations}\n')

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use this function,
        # use 'pass' instead of the following line.
        # raise NotImplementedError
        # self.fruit_locations = dict(fruits_on_board_dict)
        pass

    def fruits_life_ended(self, fruits_on_board_dict):
        if fruits_on_board_dict is not None and len(fruits_on_board_dict) > 0:
            fruit_positions = fruits_on_board_dict.keys()
            for pos in fruit_positions:
                if self.game_board[pos[0], pos[1]] > 2:
                    self.game_board[pos[0], pos[1]] = 0
            self.fruit_locations = dict()
            self.best_fruit_location = None
            self.best_fruit_value = float("-inf")

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    def utility(self, current_state):
        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                      current_state.rival_location)
        if self_moves_tuple[1] == 0 or rival_moves_tuple[1] == 0:
            if self_moves_tuple[1] > 0:
                if current_state.points > current_state.rival_points - current_state.penalty_score:
                    return 10000 + current_state.points
                    # return float("inf")
                elif current_state.points < current_state.rival_points - current_state.penalty_score:
                    return -10000 - current_state.rival_points
                    # return float("-inf")
                else:
                    return 0
            elif rival_moves_tuple[1] > 0:
                if current_state.points - current_state.penalty_score > current_state.rival_points:
                    return 10000 + current_state.points
                    # return float("inf")
                elif current_state.points - current_state.penalty_score < current_state.rival_points:
                    return -10000 - current_state.rival_points
                    # return float("-inf")
                else:
                    return 0
            else:
                if current_state.points - current_state.penalty_score > current_state.rival_points - current_state.penalty_score:
                    return 10000 + current_state.points
                    # return float("inf")
                elif current_state.points - current_state.penalty_score < current_state.rival_points - current_state.penalty_score:
                    return -10000 - current_state.rival_points
                    # return float("-inf")
                else:
                    return 0
        return 0
        # self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
        #                                                               current_state.rival_location)
        # if self_moves_tuple[1] == 0 or rival_moves_tuple[1] == 0:
        #     if self_moves_tuple[1] > 0:
        #         if current_state.points > current_state.rival_points - current_state.penalty_score:
        #             return float("inf")
        #         elif current_state.points < current_state.rival_points - current_state.penalty_score:
        #             return float("-inf")
        #         else:
        #             return 0
        #     elif rival_moves_tuple[1] > 0:
        #         if current_state.points - current_state.penalty_score > current_state.rival_points:
        #             return float("inf")
        #         elif current_state.points - current_state.penalty_score < current_state.rival_points:
        #             return float("-inf")
        #         else:
        #             return 0
        # return 0

    def is_goal(self, current_state, maximizing_player):
        self_moves_tuple, rival_moves_tuple = available_moves_handler(current_state, current_state.location,
                                                                           current_state.rival_location)
        if maximizing_player:
            if self_moves_tuple[1] == 0:
                return True
        else:
            if rival_moves_tuple[1] == 0:
                return True
        return False

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm


def state_score(board, pos):
    num_steps_available = 0
    for d in utils.get_directions():
        i = pos[0] + d[0]
        j = pos[1] + d[1]

        # check legal move
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
            num_steps_available += 1

    if num_steps_available == 0:
        return -1
    else:
        return 4 - num_steps_available


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
    total_free_cells, fruits_locations_value, fruits_concentration, player_bestfruit_manhattan_dist \
        , rival_bestfruit_manhattan_dist, fruits_locations = board_handler(state)

    ''' Calculating the quarter with the highest concentration'''
    quarter_with_highest_concentration = max(fruits_concentration, key=fruits_concentration.get)

    ''' Calculating the moves that will block some of the rival moves'''
    blocking_moves = [move for move in player_moves if move in rival_moves]

    ''' Calculating the moves that will take fruits'''
    player_moves_with_fruits = [move for move in player_moves if move in fruits_locations_value.keys()]

    ''' Calculating the total points from moves with fruits'''
    player_moves_with_fruits_points, rival_moves_with_fruits_points = 0, 0
    if len(player_moves_with_fruits) > 0:
        player_moves_with_fruits_points = sum([fruits_locations_value[move] for move in player_moves_with_fruits]) \
                                          / len(player_moves_with_fruits)


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
        moves_avg_value = sum(succs_moves_manhattan_dists.values()) / len(succs_moves_manhattan_dists)

    ''' Calculating the board size'''
    board_size = len(state.game_board) * len(state.game_board[0])


    ''' Calculating the location score like in simple player'''
    player_location_score = state_score(board=state.game_board, pos=state.location)
    rival_location_score = state_score(board=state.game_board, pos=state.rival_location)

    ''' Calculating blocked cells according to player and rival location'''
    blocked_cells = get_blocked_cells_according_to_locations(state)
    value = None
    if blocked_cells / (board_size - total_free_cells) < 0.4:
        if state.fruit_life_time > 0:
            value = ((2 * player_moves_number) - (2 * rival_moves_number)
                     + (len(blocking_moves)) + (len(successor_available_moves)) + 0.3 * state.points
                     - (1 * player_bestfruit_manhattan_dist)
                     + (2 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (0.02 * moves_avg_value)
                     + (1 * player_moves_with_fruits_points)
                     + (0.1 * player_location_score) - (0.1 * rival_location_score))
        else:
            value = (2 * player_moves_number) - (2 * rival_moves_number) \
                    + (len(blocking_moves)) + (len(successor_available_moves) + 0.1 * state.points)

    else:
        if state.fruit_life_time > 0:
            value = ((3 * player_moves_number) - (1 * rival_moves_number)
                     + (len(blocking_moves)) + (2 * len(successor_available_moves)) + 0.1 * state.points
                     - (1 * player_bestfruit_manhattan_dist)
                     + (2 * player_quarter_is_best) - (1.5 * rival_quarter_is_best) + (0.01 * moves_avg_value)
                     + (1 * player_moves_with_fruits_points)
                     + (0.1 * player_location_score) - (0.1 * rival_location_score))
        else:
            value = (3 * player_moves_number) - (1 * rival_moves_number) \
                    + (len(blocking_moves)) + (2 * len(successor_available_moves) + 0.1 * state.points)

    return value


def get_blocked_cells_according_to_locations(state):
    blocked_cells = 1
    if state.rival_location[0] > state.location[0]:
        start_row = state.location[0]
        end_row = state.rival_location[0]
    else:
        start_row = state.rival_location[0]
        end_row = state.location[0]
    if state.rival_location[1] > state.location[1]:
        start_col = state.location[1]
        end_col = state.rival_location[1]
    else:
        start_col = state.rival_location[1]
        end_col = state.location[1]
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if state.game_board[row][col] != 0 and state.game_board[row][col] <= 2:
                blocked_cells += 1
    return blocked_cells


def get_manhattan_dists_for_succ(succ_moves, state):
    dists = dict()
    for move in succ_moves:
        manhattan_val = manhattan_distance(move, state.best_fruit_location)
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


def sync_objects(first_object, game_board, location, points, fruit_life_time, fruit_locations,
                 best_fruit_location, best_fruit_value):
    first_object.location = copy.deepcopy(location)
    first_object.game_board = copy.deepcopy(game_board)
    first_object.points = copy.deepcopy(points)
    first_object.fruit_life_time = copy.deepcopy(fruit_life_time)
    # if fruit_locations is not None and len(fruit_locations) >= 0:
    first_object.fruit_locations = copy.deepcopy(fruit_locations)
    first_object.best_fruit_value = copy.deepcopy(best_fruit_value)
    first_object.best_fruit_location = copy.deepcopy(best_fruit_location)