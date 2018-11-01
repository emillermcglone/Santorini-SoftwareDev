# Class that parses the given test input into the format that we want
from Admin.board import GameBoard
from Common.command_handler import Cmd_Handler
from Player.test_message_funcs import *


class Board_Tester():
    """
    Class to parse test input and get output for a board
    """
    def __init__(self):
        """
        Initializes a board test parser
        """
        self.board = GameBoard()
        self.__cmd_handler = Cmd_Handler(lambda x: x[0])
        self.__cmd_handler.register_cmd("move", lambda x: board_move(x, self))
        self.__cmd_handler.register_cmd("build", lambda x: board_build(x, self))
        self.__cmd_handler.register_cmd("neighbors", lambda x: neighbors_func(x, self))
        self.__cmd_handler.register_cmd("occupied?", lambda x: occupied_func(x, self))
        self.__cmd_handler.register_cmd("height", lambda x: height_func(x, self))

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
