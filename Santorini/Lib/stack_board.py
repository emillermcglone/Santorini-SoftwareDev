# class that allows a board to act like a stack by pushing and poppping
# delta transitions for board state
from Common.command_handler import Cmd_Handler


class StackBoard:
    """ Class that allowd interaction to happend with a GameBoard like a stack using actions"""
    def __init__(self, board):
        """
        Initializes a StackBoard

        :param board: A GameBoard
        Attributes:
            _action_storage: list of actions on this 'stack'
            __fwd_cmd: How to deal with an action while pushing
            __rev_cmd: how to deal with an action while popping
        """
        self._action_storage = []
        self.board = board

        fwd_cmd = Cmd_Handler(lambda x: x['type'])
        fwd_cmd.register_cmd('place', self.__place_worker)
        fwd_cmd.register_cmd('move', self.__move_worker)
        fwd_cmd.register_cmd('build', self.__build_floor)
        self.__fwd_cmd = fwd_cmd

        rev_cmd = Cmd_Handler(lambda x: x['type'])
        rev_cmd.register_cmd('place', self.__remove_worker)
        rev_cmd.register_cmd('move', self.__reverse_worker)
        rev_cmd.register_cmd('build', self.__remove_floor)
        self.__rev_cmd = rev_cmd

    def isEmpty(self):
        """ Check to see if our 'stack' is empty"""
        return len(self._action_storage) == 0

    def push(self, action):
        """
        Push a action onto the stack and mutate board

        :param action: JSON value representing any action
        """
        self.__fwd_cmd.handle_cmd(action)
        self._action_storage.append(action)

    def pop(self):
        """
        Pop a action onto the stack and mutate board

        :return: JSON value representing any action
        """
        action = self._action_storage.pop()
        self.__rev_cmd.handle_cmd(action)
        return action

    def __place_worker(self, action):
        """
        Place a worker on the board

        :param action: JSON value representing a place action
        """
        pid = action['pid']
        wid = action['wid']
        x, y = action['xy']
        self.board.place_worker(pid, wid, x, y)

    def __remove_worker(self, action):
        """
        Remove a worker on the board

        :param action: JSON value representing a place action
        """
        x, y = action['xy']
        self.board.place_worker(None, None, x, y)

    def __move_worker(self, action):
        """
        Move a worker on the board

        :param action: JSON value representing a move action
        """
        x1, y1 = action['xy1']
        x2, y2 = action['xy2']
        self.board.move_worker(x1, y1, x2, y2)

    def __reverse_worker(self, action):
        """
        Move a worker in reverse on the board

        :param action: JSON value representing a move action
        """
        x1, y1 = action['xy2']
        x2, y2 = action['xy1']
        self.board.move_worker(x1, y1, x2, y2)

    def __build_floor(self, action):
        """
        Build a floor a cell on the board

        :param action: JSON value representing a build action
        """
        x, y = action['xy2']
        self.board.build_floor(x, y)

    def __remove_floor(self, action):
        """
        Remove a floor on a cell on the board

        :param action: JSON value representing a build action
        """
        x, y = action['xy2']
        self.board.build_floor(x, y, -1)
