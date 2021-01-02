"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
# TODO: you can import more modules, if needed
import numpy as np
import copy
from players import MinimaxPlayer
from players import AlphabetaPlayer


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal):
        """The constructor for all the search algos.
        You can code these functions as you like to,
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.

        # if MinimaxPlayer.Player.check_time():
        #     MinimaxPlayer.Player.time_ended = True
        # if MinimaxPlayer.Player.time_ended:
        #     return -1
        if self.goal(state):
            val = self.utility(state), None
            # print(f'In Goal State ,maximizing_player={maximizing_player}, Utility value is:{val}\n')
            return val
        if depth == 0:
            val = MinimaxPlayer.heuristic(state), None
            # print(f'In Depth 0 ,maximizing_player={maximizing_player}, Heuristic value is:{val}\n')
            return val

        available_moves = MinimaxPlayer.get_moves_from_location(state, maximizing_player)
        max_result = float("-inf")
        min_result = float("inf")
        selected_move = None
        # print(f'In Depth = {depth} ,maximizing_player={maximizing_player}, available_moves:{available_moves}\n')
        for move in available_moves:
            # print(f'In Depth = {depth} ,maximizing_player={maximizing_player}, player making move:{move}\n')
            state.make_move(move, maximizing_player)
            move_value = self.search(copy.deepcopy(state), depth - 1, not maximizing_player)
            state.undo_move(move, maximizing_player)
            # print(f'In Depth = {depth} ,maximizing_player={maximizing_player}, player undoing move:{move}\n')
            if maximizing_player and max_result < move_value[0]:
                # print(f'In Depth = {depth} ,maximizing_player={maximizing_player},\n'
                #       f'new max value is:{move_value[0]} and selected move is:{move}\n')
                max_result = move_value[0]
                selected_move = move
            elif not maximizing_player and min_result > move_value[0]:
                # print(f'In Depth = {depth} ,maximizing_player={maximizing_player},\n'
                #       f'new min value is:{move_value[0]} and selected move is None\n')
                min_result = move_value[0]

        if maximizing_player:
             # print(f'In Depth = {depth} ,maximizing_player={maximizing_player},\n'
             #       f'The selected max value is:{max_result} and selected move is:{selected_move}\n')
             return max_result, selected_move
        else:
             # print(f'In Depth = {depth} ,maximizing_player={maximizing_player},\n'
             #       f'The selected min value is:{min_result} and selected move is None\n')
             return min_result, None


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        # raise NotImplementedError
        if self.goal(state):
            val = self.utility(state), None
            # print(f'In Goal State ,maximizing_player={maximizing_player}, Utility value is:{val}\n')
            return val
        if depth == 0:
            val = MinimaxPlayer.heuristic(state), None
            # print(f'In Depth 0 ,maximizing_player={maximizing_player}, Heuristic value is:{val}\n')
            return val

        available_moves = MinimaxPlayer.get_moves_from_location(state, maximizing_player)
        max_result = float("-inf")
        min_result = float("inf")
        selected_move = None

        for move in available_moves:

            state.make_move(move, maximizing_player)
            move_value = self.search(copy.deepcopy(state), depth - 1, not maximizing_player, alpha, beta)
            state.undo_move(move, maximizing_player)

            # if move_value[0] == np.inf or move_value[0] == -np.inf:
            #     break

            if maximizing_player and max_result < move_value[0]:
                max_result = move_value[0]
                selected_move = move
                alpha = max(move_value[0], alpha)
                if alpha >= beta:
                    break
                    # return np.inf, None

            elif (not maximizing_player) and (min_result > move_value[0]):
                min_result = move_value[0]
                beta = min(move_value[0], beta)
                if alpha >= beta:
                    break
                    # return -np.inf, None

        if maximizing_player:
            return max_result, selected_move

        else:
            return min_result, None
