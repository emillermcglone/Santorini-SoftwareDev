import json

from Common.player import Player as IPlayer

class RemotePlayer(IPlayer):
    """ Remote player over TCP connection """

    def __init__(self, player_id, connection, buffer_size = 1024):
        """
        Initialize RemotePlayer with live TCP connection.

        :param connection: conn, live TCP connection from socket
        """
        self.__id = player_id
        self.__connection = connection
        self.buffer_size = buffer_size


    def get_id(self):
        return self.__id


    def set_id(self, new_id):
        self.__id = new_id
        self.__send(["playing-as", new_id])


    def notify_of_opponent(self, opponent_id):
        try:
            self.__send(opponent_id)
        except:
            return
            

    def get_placement(self, board, wid, rule_checker):
        workers = board.find_workers()
        worker_places = list(map(lambda w: self.__get_worker_place(board, *w), workers))

        self.__send(worker_places)
        response = self.__receive()
        return {'type': 'place', 'wid': wid, 'xy': response }


    def get_move(self, board, rule_checker):
        move, build = self.__get_move_and_build(board)
        self.last_build = build
        return move

    def get_build(self, board, wid, rule_checker):
        return self.last_build

    def game_over(self, status):
        try:
            self.__send(status)
        except:
            return


    def disconnect(self):
        """ 
        Disconnect TCP from this Player.
        """
        self.__connection.close()    

    
    def __send(self, message):
        """
        Send message over TCP.

        :param message: string, message to send
        """
        message = json.dumps(message)
        self.__connection.sendall(message.encode())


    def __receive(self):
        """
        Receive message from TCP.

        :return: string, message received from TCP.
        """
        return json.loads(self.__connection.recv(self.buffer_size).decode())


    def __get_worker_place(self, board, x, y):
        """
        Format the worker placement as [Worker, Coordinate, Coordinate]
        
        :param board: GameBoard, copy of the current state of the game 
        :param x: N, x coordinate of the position of the worker
        :param y: N, y coordinate of the position of the worker 

        :return: WorkerPlace 
        """
        return [board.get_worker_id(x, y), x, y]


    def __get_move_and_build(self, board):
        """
        Send the board and receive the turn action. 
        Format the turn action into move action and build action.
        
        :param board: GameBoard, copy of the current state of the game 
        
        :return: MoveAction, BuildAction
        """
        json_board = self.__make_board(board)
        self.__send(json_board)
        move_and_build = self.__receive()

        wid = move_and_build[0]
        move_east_west = move_and_build[1]
        move_north_south = move_and_build[2]
        build_east_west = move_and_build[3]
        build_north_south = move_and_build[4]

        
        move_from, move_to = self.__get_origin_and_next_position(board, wid, move_east_west, move_north_south)
        move = {'type': 'move', 'xy1': list(move_from), 'xy2': list(move_to)}
        
        build_to = self.__get_next_position(*move_to, build_east_west, build_north_south)
        build = {'type': 'build', 'xy1': list(move_to), 'xy2': list(build_to)}

        return move, build


    def __get_origin_and_next_position(self, board, wid, eastwest, northsouth):
        """
        Get the current position of worker and the next in the given directions. 

        :param board: GameBoard, the game board
        :param wid: string, worker id
        :param eastwest: EastWest, east or west
        :param northsouth: NorthSouth, north or south 
        :return: ((N, N), (N, N)), origin coordinates and next coordinates
        """
        worker_x, worker_y = board.find_worker(self.__id, wid)
        next_position = self.__get_next_position(worker_x, worker_y, eastwest, northsouth)
        return (worker_x, worker_y), next_position

    
    def __get_next_position(self, x, y, eastwest, northsouth):
        """
        Get next position in given direction from original coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :param eastwest: EastWest, east or west
        :param northsouth: NorthSouth, north or south 
        :return: (N, N), new coordinates
        """
        new_y = self.__north_south_position(y, northsouth)
        new_x = self.__east_west_position(x, eastwest)

        return new_x, new_y
        

    def __north_south_position(self, y, northsouth):
        """
        Get new coordinate given north or south position 
        
        :param y: y coordinate
        :param northsouth: NorthSouth, North, South, or Put
        :return: N, new y coordinate
        """
        if northsouth == "PUT":
            return y
        elif northsouth == "NORTH":
            return y - 1
        elif northsouth == "SOUTH":
            return y + 1
            

    def __east_west_position(self, x, eastwest):
        """
        Get new coordinate given east or west direction.

        :param x: N, x coordinate
        :param eastwest: EastWest, East, West, or Put
        :return: N, new x coordinate
        """
        if eastwest == "PUT":
            return x
        elif eastwest == "EAST":
            return x + 1
        elif eastwest == "WEST":
            return x - 1
        
    def __make_board(self, board):
        """
        Given a GameBoard, make a JSON representation of it. 

        :param board: GameBoard, game board
        :return: Board, as specified in remote protocol
        """
        board = [[self.__cell(board.get_height(x, y), board.get_player_id(x, y), board.get_worker_id(x, y)) for x in range(6)] for y in range(6)]
        return board

    
    def __cell(self, height, player_id, worker_id):
        """
        Given cell information, reformat into JSON representation.

        :param height: N, height of cell
        :param player_id: string, id of player
        :param worker_id: string, id of worker
        :return: Cell, as specified in remote protocol
        """
        if player_id is None:
            return height
        return "{}{}{}".format(height, player_id, worker_id)