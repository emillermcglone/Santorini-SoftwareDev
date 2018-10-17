# Class that allows for generic command handling


class Cmd_Handler():
    """
    Class to implement generic interpreter pattern

    Attributes:
        __cmd_selector: Function to get the type of the cmd
        __cmd_map:      map that holds {type: function_to_run}
    """
    def __init__(self, selector=None):
        """
        Initializes a cmd_handler

        :param selector: Function that will return the appropriate part of the message to discriminate against
        """
        self.__cmd_selector = selector
        self.__cmd_map = {}

    def set_selector(self, selector):
        """
        Setter for selector

        :param selector: Function that will return the appropriate part of the message to discriminate against
        """
        self.__cmd_selector = selector

    def register_cmd(self, cmd, func):
        """
        Allows registration of a type of a cmd to a function to run for that cmd

        :param cmd:     type of command
        :param func:    function to run to handle the given command
        """
        self.__cmd_map[cmd] = func

    def handle_cmd(self, cmd):
        """
        Handle an actual cmd message

        :param cmd:     message that is the command to handle
        """
        return self.__cmd_map[self.__cmd_selector(cmd)](cmd)
