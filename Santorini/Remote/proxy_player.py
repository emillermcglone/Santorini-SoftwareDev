import json
import copy
from Admin.board import GameBoard
from Admin.rule_checker import RuleChecker


class ProxyPlayer:
    """
    Proxy player decorator for a Player component.
    """

    def __init__(self, player, proxy):
        """
        Initialize ProxyPlayer with player component and client proxy 
        to interact with server.

        :param player: Player, player component
        :param proxy: ClientProxy, proxy between player and server
        """
        self.player = player
        self.proxy = proxy
        self.board = GameBoard()
        self.rule_checker = RuleChecker(self.board)
        self.opponent = None

        self.workers = []


    @property
    def player_id(self):
        return self.player.get_id()


    def run(self):
        self.__send(self.player.get_id())
        self.proxy.subscribe(self.__handle_message, )

    def __send(self, value):
        """
        Send JSONified value to server.

        :param value: Any, value that can be JSONified
        """
        message = json.dumps(value)
        self.proxy.send(message)


    def __receive(self):
        """
        Receive JSON loaded value from server.

        :return: Any, JSON loaded value from server
        """
        response = self.proxy.receive()
        return json.loads(response)

        
    def __handle_message(self, response):
        qualifier_to_handlers = {
            self.__playing_as_qualifier: self.__playing_as_handler,
            self.__opponent_qualifier: self.__opponent_handler,
            self.__placement_qualifier: self.__placement_handler,
            self.__turn_qualifier: self.__turn_handler,
        }

        for qualifier, handler in qualifier_to_handlers.items():
            if qualifier(response):
                handler(response)
                return

        self.__send(self.player_id)
            

    def __playing_as_qualifier(self, value):
        """ 
        Check that value is a playing as message

        :param value: Any, value to check
        :return: bool, True if value is a playing as message, False otherwise
        """
        return isinstance(value, list) and value[0] == "playing-as" and isinstance(value[1], str)


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

        :param value: Placement, placement message
        """
        if len(value) >= 2:
            self.workers.append(value[])


        for w in value:
            wid, x, y = w
            if wid in self.workers:
                self.board.place_worker(self.player_id, wid, x, y)
            else:
                self.board.place_worker(self.opponent, wid, x, y)

        spec = self.player.get_placement(self.board, "id", self.rule_checker)
        self.__send(spec['xy'])


    def __turn_qualifier(self, value):
        """
        Check if value is a turn request message.

        :param value: Any, value to check
        :return: bool, True if value is a turn request, False otherwise
        """
        len_six_internally = all(map(lambda v: len(v) == 6, value))
        return isinstance(value, list) and len(value) == 6 and len_six_internally


    def __turn_handler(self, value):
        """
        Handle turn message.

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
        gb = GameBoard()
        for y, row in enumerate(board):
            for x, el in enumerate(row):
                if isinstance(el, int):
                    gb.build_floor(x, y, el)
                elif isinstance(el, str):
                    height = int(el[0])
                    pid = el[1:-1]
                    wid = el[-1]
                    self.board.build_floor(x, y, height)
                    self.board.place_worker(pid, wid, x, y)
        return gb


    def __natural_under_five(self, value):
        return isinstance(value, int) and value >= 0 and value <= 5


    def __handle_connection_loss():
        pass


    def __get_direction(self, from_xy, to_xy):
        from_x, from_y = from_xy
        to_x, to_y = to_xy
    
        return [self.__east_west(from_x, to_x), self.__north_south(from_y, to_y)]

    
    def __north_south(self, from_y, to_y):
        if to_y is from_y:
            return "PUT"
        elif to_y > from_y:
            return "SOUTH"
        else:
            return "NORTH"


    def __east_west(self, from_x, to_x):
        if to_x is from_x:
            return "PUT"
        elif to_x > from_x:
            return "EAST"
        else:
            return "WEST"


