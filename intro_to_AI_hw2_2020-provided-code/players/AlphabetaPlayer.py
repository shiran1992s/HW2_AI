"""
MiniMax Player with AlphaBeta pruning
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.penalty_score = penalty_score
        self.location = None
        self.game_board = None
        self.rival_location = None
        self.rival_points = 0
        self.points = 0
        self.time_ended = False
        self.start_time = 0
        self.fruit_locations = dict()
        self.fruit_locations_life_time = dict()  # TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
        self.best_fruit_value = 0
        self.best_fruit_location = None
        self.moves_available = []
        self.moves_available_count = 0
        self.rival_moves_available = []
        self.rival_moves_available_count = 0
        self.min_dimention = None  # TODO: IF NOT USED REMOVE ITS FOR FRUITS_LIFE_TIME
        self.fruits_concentration = None
        self.init_concentration_dict()

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        #TODO: erase the following line and implement this function.

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
                    self.fruit_locations_life_time.update(
                        {location: self.min_dimention})  # TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
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
        #TODO: define alfa=-np.inf, beta=np.inf and use them................

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
        #TODO: erase the following line and implement this function. In case you choose not to use this function, 
        # use 'pass' instead of the following line.

        # TODO: IF NOT USED REMOVE FRUITS_LIFE_TIME
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

    def utility(self, current_state):

        self_moves_tuple, rival_moves_tuple = self.available_moves_handler(current_state.location,
                                                                           current_state.rival_location)

        if self_moves_tuple[1] is 0 and self.rival_moves_tuple[1] is 0:
            return 0
        if self.self_moves_tuple[1] >= 1:
            return 1
        return -1


    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm

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