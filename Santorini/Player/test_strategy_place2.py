# This file implements the place furthest strategy spec'd out for assignment 8
from Common.command_handler import Cmd_Handler


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
        cmd_handler.register_cmd('place', self.decide_place)
        self.__cmd_handler = cmd_handler

        if not init:
            self.init_state(init)
        else:
            self.__state = None

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
            self.__state = board
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

        :param action: JSON that represents an place action
        """

        wid = action['wid']
        opponent_workers = []

        for cell in self.__state.board.find_workers():
            if not self.__state.board.get_player_id(cell[0], cell[1]) == self.__pid:
                opponent_workers.append(cell)

        corners = [(0, 0), (5, 0), (0, 5), (5, 5)]

        max_dist = float('-inf')
        max_corner = None
        for c in corners:
            for worker in opponent_workers:
                dist = math.hypot(abs(worker[0] - c[0]), abs(worker[1] - c[1]))
                if dist > max_dist:
                    max_dist = dist
                    max_corner = c

        self.__state.board.place_worker(self.__pid, wid, c[0], c[1])
        return True

    def decide_move(self, action):
        """
        Method that makes a decision about where to make the next move

        :param action: JSON that represents a move action
        """
        pass

    def decide_build(self, action):
        """
        Method that makes a decision about where to build

        :param action: JSON that represents a build action
        """
        pass
