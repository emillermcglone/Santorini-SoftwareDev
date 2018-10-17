# Class that parses the given test input into the format that we want
from Santorini.Common.board import GameBoard
from Santorini.Player.test_strategy_alive import Strategy
from Santorini.Common.command_handler import Cmd_Handler
from Santorini.Player.test_message_funcs import *


class Strategy_Tester():
    """
    Class to parse test input and get output for a strategy
    """
    def __init__(self, pid):
        """
        Initializes a strategy test parser
        """
        self.board = GameBoard()
        self.strategy = Strategy(pid, init=self.board)
        self.__cmd_handler = Cmd_Handler(lambda x: x[0])
        self.__cmd_handler.register_cmd("move", lambda x: strat_move(x, self))
        self.__cmd_handler.register_cmd("+build", lambda x: strat_build(x, self))
        self.prev_move = None

    def set_board(self, cells):
        """
        Sets up the board to be used with this test parser

        :param cells:   JSON representing the state of the board from given spec
        """
        build_board(cells, self)

    def parse(self, cmd):
        """
        Parses the given command and invokes the appropriate function to run

        :param cmd: JSON that represents a valid query according to given spec
        """
        return self.__cmd_handler.handle_cmd(cmd)