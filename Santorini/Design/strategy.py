# This file describes what a strategy object should look like and
# how we expect it to interact with Santorini. The idea where is that by
# using Queues for input and output we decouple it from whatever mechanism
# they are using to communicate and leave that to implementation a level above


class Strategy:
    """
    Class representing a Santorini Strategy

    Attributes:
        __player_id:    String that represents this player on the board
        __in_q:         Queue where the strategy can expect to receive input from Santorini
        __out_q:        Queue where the strategy can push actions to and expect Santorini to read
        __cmd_handler:  A Command_Handler that will be able to parse messages
        __state:        Variable that hols state of the game. Up to implementation to decide
                        on the structure as different strategies may benefit from different types
    """

    def __init__(self, in_q, out_q):
        """
        Initializes a strategy object for use

        :param in_q:    Queue to check for messages
        :param out_q:   Queue to push action messages to
        """
        pass

    def __read_msg(self):
        """
        Checks the in_q for messages

        Reads in the next message, passes the information to the action handling function
        """
        pass

    def __write_message(self, msg):
        """
        Pushes the given message into the out_q

        :param msg:     JSON encoded message that represents an action
        """
        pass

    def update_state(self, dstate):
        """
        Updates internal state for decision making

        :param dstate:  JSON encoded value that represents a delta for updating the internal state
        """
        pass

    def decide_place(self, wid):
        """
        Method that makes a decision about worker placement

        :param wid:     Identifier for the worker to place
        """
        pass

    def decide_move(self):
        """
        Method that makes a decision about where to make the next move
        """
        pass

    def decide_build(self, wid):
        """
        Method that makes a decision about where to build

        :param wid:     Identifier for a worker that needs to build
        """
        pass
