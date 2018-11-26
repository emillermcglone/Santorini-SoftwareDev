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


    def get_id(self):
        return self.__id


    def set_id(self, new_id):
        self.__id = new_id
        self.__send(["playing as", new_id])
            

    def get_placement(self, board, wid, rule_checker):
        workers = board.find_workers()
        worker_places = list(map(lambda w: self.get_worker_place(board, *w), workers))
        self.__send(worker_places)
        response = self.__receive()
        return {'type': 'place', 'wid': wid, 'xy': response }


    def get_worker_place(self, board, x, y):
        return [board.get_worker_id(x, y), x, y]


    def get_move(self, board, rule_checker):
        pass

    def get_build(self, board, wid, rule_checker):
        pass

    def game_over(self, status):
        pass
        
