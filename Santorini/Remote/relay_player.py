import json
import copy
from Admin.board import GameBoard
from Admin.rule_checker import RuleChecker
import sys
import threading

from pprint import pprint

class RelayPlayer:
    """
    Proxy player decorator for a Player component.
    """

    def __init__(self, player, relay):
        """
        Initialize RelayPlayer with player component and client relay 
        to interact with server.

        :param player: Player, player component
        :param relay: Relay, relay between player and server
        """
        self.player = player
        self.relay = relay

        self.board = GameBoard()
        self.rule_checker = RuleChecker(self.board)

        self.opponent = None
        self.workers = []


    @property
    def player_id(self):
        """
        Player id of this player.

        :return: string, id of player
        """
        return self.player.get_id()


    def run(self):
        """ Run RelayPlayer, sending player id and subscribing to Relay. """
        self.__send(self.player.get_id())
        self.relay.subscribe(self.__handle_message, self.__handle_connection_loss)


    def __send(self, value):
        """
        Send JSONified value to server.

        :param value: Any, value that can be JSONified
        """
        message = json.dumps(value)
        self.relay.send(message)


    def __receive(self):
        """
        Receive JSON loaded value from server.

        :return: Any, JSON loaded value from server
        """
        response = self.relay.receive()
        return json.loads(response)

        
    def __handle_message(self, response):
        """
        Handle message from server. If message doesn't correspond to any 
        qualifier, send server player id to give up.

        :param response: Any, message from server.
        """
        qualifier_to_handlers = {
            self.__playing_as_qualifier: self.__playing_as_handler,
            self.__opponent_qualifier: self.__opponent_handler,
            self.__placement_qualifier: self.__placement_handler,
            self.__turn_qualifier: self.__turn_handler,
            self.__results_qualifier: self.__results_handler,
        }

        for qualifier, handler in qualifier_to_handlers.items():
            if qualifier(response): 
                handler(response)
                return

        # if no qualifier validates message, give up.
        self.__send(self.player_id)


    def __results_qualifier(self, value):
        """
        Check if given value is a Results message.
        
        :param value: Any, value to check
        :return: bool, True if value is a Results message, False otherwise
        """
        def is_encounter_outcome(value):
            return isinstance(value, list) and (len(value) == 2 or len(value) == 3) \
                and isinstance(value[0], str) and isinstance(value[1], str)

        return isinstance(value, list) and all(map(is_encounter_outcome, value))

    
    def __results_handler(self, value):
        """
        Handle Results message by doing nothing.

        :param value: Results, results message
        """
        pass


    def __handle_connection_loss(self):
        """
        Handle connection loss by closing relay.
        """
        self.relay.close()
            

    def __playing_as_qualifier(self, value):
        """ 
        Check that value is a playing as message

        :param value: Any, value to check
        :return: bool, True if value is a playing as message, False otherwise
        """
        return isinstance(value, list) and len(value) == 2 and value[0] == "playing-as" and isinstance(value[1], str)


    def __playing_as_handler(self, value):
        """
        Handle playing as message

        :param value: ["playing-as", string], playing as message
        """
        self.player.set_id(value[1])

    
    def __opponent_qualifier(self, value):
        """ 
        Check that value is an opponent id message

        :param value: Any, value to check
        :return: bool, True if value is an opponent id message, False otherwise
        """
        return isinstance(value, str)


    def __opponent_handler(self, value):
        """
        Handle opponent id message.

        :param value: string, opponent id message
        """
        self.opponent = value


    def __placement_qualifier(self, value):
        """
        Check that value is the Placement message.

        :param value: Any, value to check
        :return: bool, True if value is Placement message, False otherwise
        """

        def is_worker_place(value):
            return isinstance(value, list) and len(value) == 3 and isinstance(value[0], str) and (
                self.__natural_under_five(value[1]) and self.__natural_under_five(value[2]))
        
        return isinstance(value, list) and all(map(is_worker_place, value))


    def __placement_handler(self, value):
        """
        Handle Placement message.

        Replace all the workers in the board. 

        :param value: Placement, placement message
        """

        # if there's more than 2 workers, add second last worker to list
        # because that's the worker this player owns.
        # This is necessary because our player is designed to receive
        # worker ids for placement request but instead, the server
        # assigns the worker id AFTER the placement. 
        if len(value) >= 2:
            self.workers.append(self.__get_second_to_last(value)[0])
        
        # if there's less than 2, reset worker list
        else:
            self.workers = []

        for worker_place in value:
            wid, x, y = worker_place
            if wid in self.workers:
                self.board.place_worker(self.player_id, wid, x, y)
            else:
                self.board.place_worker(self.opponent, wid, x, y)

        spec = self.player.get_placement(self.board, "id", self.rule_checker)
        self.__send(spec['xy'])


    def __get_second_to_last(self, l):
        """
        Get the second to last element from given list.

        :param l: [Any, ...], list
        :return: Any, the second to last element
        """
        return l[-2]


    def __turn_qualifier(self, value):
        """
        Check if value is a turn request message.

        :param value: Any, value to check
        :return: bool, True if value is a turn request, False otherwise
        """
        def len_six_internally(row):
            return all(map(lambda v: len(v) == 6, row))
        return isinstance(value, list) and len(value) == 6 and len_six_internally(value)


    def __turn_handler(self, value):
        """
        Handle turn message.

        Remake board according to Board specification from server.

        :param value: Board, board
        """
        self.board = self.__make_game_board(value)
        self.rule_checker = RuleChecker(self.board)

        move = self.player.get_move(self.board, self.rule_checker)

        copy_board = copy.deepcopy(self.board)
        copy_rule_checker = RuleChecker(copy_board)
        wid = copy_board.get_worker_id(*move['xy1'])
        copy_board.move_worker(*move['xy1'], *move['xy2'])

        build = self.player.get_build(copy_board, wid, copy_rule_checker)

        move_EW, move_NS = self.__get_direction(move['xy1'], move['xy2'])
        build_EW, build_NS = self.__get_direction(build['xy1'], build['xy2'])
        request = [wid, move_EW, move_NS, build_EW, build_NS]
        self.__send(request)


    def __make_game_board(self, board):
        """
        Make a GameBoard from the Board specification.

        :param board: Board, board state specification from server.
        :return: GameBoard, the GameBoard from the Board specification
        """
        gb = GameBoard()
        for y, row in enumerate(board):
            for x, el in enumerate(row):

                # if there's no worker
                if isinstance(el, int):
                    gb.build_floor(x, y, el)

                # if there's a worker
                elif isinstance(el, str):
                    height = int(el[0])
                    pid = el[1:-1]
                    wid = el[-1]
                    gb.build_floor(x, y, height)
                    gb.place_worker(pid, wid, x, y)
        return gb


    def __natural_under_five(self, value):
        """
        Is given value a natural number under five?

        :param value: Any, value to check
        :return: bool, True if natural number under five, False otherwise
        """
        return isinstance(value, int) and value >= 0 and value <= 5


    def __get_direction(self, from_xy, to_xy):
        """
        Get directions from coordinates.

        :param from_xy: (N, N), from coordinates
        :param to_xy: (N, N), to coordinates
        :return: [string, string], directions 
        """
        from_x, from_y = from_xy
        to_x, to_y = to_xy

        return [self.__east_west(from_x, to_x), self.__north_south(from_y, to_y)]

    
    def __north_south(self, from_y, to_y):
        """
        Get y direction.

        :param from_y: N, y from coordinate
        :param to_y: N, y to coordinate
        :return: string, direction
        """
        if to_y == from_y:
            return "PUT"
        elif to_y > from_y:
            return "SOUTH"
        else:
            return "NORTH"


    def __east_west(self, from_x, to_x):
        """
        Get x direction.

        :param from_x: N, x from coordinate
        :param to_x: N, x to coordinate
        :return: string, direction
        """
        if to_x == from_x:
            return "PUT"
        elif to_x > from_x:
            return "EAST"
        else:
            return "WEST"
