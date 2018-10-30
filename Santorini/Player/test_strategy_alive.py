# This file implements the strategy spec'd out for assignment 8
from Common.command_handler import Cmd_Handler
from Lib.stack_board import StackBoard
from Common.rule_checker import RuleChecker
from Lib.util import gen_builds, gen_moves


class Strategy:
    """
    Class representing a Santorini Strategy

    Attributes:
        __pid           Player ID string
        __cmd_handler:  A Command_Handler that will be able to parse messages
        __state:        Variable that holds state of the game. Up to implementation to decide
                        on the structure as different strategies may benefit from different types
    """

    def __init__(self, pid, init=None):
        """
        Initializes a strategy object for use

        :param pid:     String identifing a player
        :param init:    Optional Santoini GameBoard that represents initial state
        """
        self.__pid = pid

        cmd_handler = Cmd_Handler(lambda x: x['type'])
        cmd_handler.register_cmd('build', self.decide_build)
        cmd_handler.register_cmd('move', self.decide_move)
        self.__cmd_handler = cmd_handler

        self.__opponent = None
        self.look_ahead = 0

        self.__state = None

        if init:
            self.init_state(init)

    def get_result(self, action):
        """
        Uses instance specific command handler to determine how optimize for given action

        :param action: JSON that represents an action
        """
        return self.__cmd_handler.handle_cmd(action)

    def init_state(self, board):
        """
        Allows for the initialization of a internal state based off of a GameBoard

        :param board: a Santorini GameBoard that represents the initial state for this trategy
        """
        if not self.__state:
            self.__state = StackBoard(board)
            self.checker = RuleChecker(board)
            return True
        return False

    def update_state(self, dstate):
        """
        Updates internal state for decision making

        :param dstate:  JSON encoded value that represents a delta for updating the internal state
        """
        pass

    def decide_place(self, action):
        """
        Method that makes a decision about worker placement

        :param action:     JSON representing a place action
        """
        pass

    def decide_move(self, action):
        """
        Method that makes a decision about where to make the next move
        """
        x1, y1 = action['xy1']
        x2, y2 = action['xy2']
        self.__state.push(action)

    def other_player(self, player):
        """
        Get the other player from the given one
        :param player: Player ID
        """
        if player == self.__opponent:
            return self.__pid
        else:
            return self.__opponent

    def check_move_states(self, player, depth):
        """
        Check all possible move states at this layer
        :param player: Player ID
        :param depth: current tree depth
        """

        if depth >= self.look_ahead:
            return True

        for move in gen_moves(player, self.__state.board, self.checker):
            self.__state.push(move)
            winner = self.checker.check_game_over(self.__pid, self.__opponent)
            if winner == self.__opponent:
                return False
            worker = move['xy2']
            if not self.check_build_states(player, worker, depth):
                return False
            self.__state.pop()
        return True

    def check_build_states(self, player, worker, depth):
        """
        Check all possible build states at this layer
        :param player: Player ID
        :param worker: worker as (x, y)
        :param depth: current tree depth
        """

        if depth >= self.look_ahead:
            return True

        for build in gen_builds(player, worker, self.__state.board, self.checker):
            self.__state.push(build)
            winner = self.checker.check_game_over(self.__pid, self.__opponent)
            if winner == self.__opponent:
                return False
            if not self.check_move_states(self.other_player(player), depth + 1):
                return False
            self.__state.pop()
        return True

    def get_opponent(self):
        """ Gets the player that does not belong to this strategy"""
        for cell in self.__state.board.find_workers():
            player = self.__state.board.get_player_id(cell[0], cell[1])
            if not player == self.__pid:
                return player

    def decide_build(self, action):
        """
        Method that makes a decision about where to build

        :param action:  JSON that represents a build action
        """

        # Mutate board into starting search state
        x1, y1 = action['xy1']
        x2, y2 = action['xy2']
        self.__state.push(action)

        self.__opponent = self.get_opponent()
        current_player = self.__opponent

        self.checker.current_player = self.__pid
        winner = self.checker.check_game_over(self.__pid, self.__opponent)
        if winner == self.__opponent:
                return False
        alive = self.check_move_states(current_player, 1)
        return alive