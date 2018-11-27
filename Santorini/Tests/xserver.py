"""
XServer starts up a Santorini game server that hosts a tournament among remote players 
through TCP connections. 
"""

import sys
import socket
import json
import fileinput


from threading import Thread
from timeout_decorator import timeout, TimeoutError
import names

sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from Admin.server_configurations.stdin_server_configuration import ServerConfiguration
from Admin.tournament_manager import TournamentManager
from Admin.configuration import IConfiguration
from Remote.remote_player import RemotePlayer

from pprint import pprint

class TournamentManagerConfiguration:
    def __init__(self, players):
        self.__players = players
    
    def players(self):
        return self.__players

    def observers(self):
        return []


class XServer:
    """ Server to host Santorini game among remote players connected through TCP. """

    def __init__(self, configuration=ServerConfiguration()):
        """
        Initialize XServer with server configuration.

        :param configuration: ServerConfiguration, server configuration
        """
        self.ip = 'localhost'
        self.buffer_size = 1024

        self.min_players = configuration.min_players()
        self.port = configuration.port()
        self.waiting_for = configuration.waiting_for()
        self.repeat = configuration.repeat()
        
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.ip, self.port))

        self.players = []


    def __reset(self):
        """
        Reset the server after a tournament has ended or when not enough players connect.

        Players are disconnected. The socket is closed if the tournament should not be repeated, repeat is 0. 
        """
        for p in self.players:
            p.disconnect()
        self.players = []

        if not self.repeat:
            self.close()
            sys.exit()


    def start(self):
        """
        Start server and spin up a new thread for it. 
        """
        self.__socket.listen(3)
        self.live = True

        self.__accept_connections()

        if len(self.players) < self.min_players:
            self.__reset()
            return self.start() # return to avoid stack overflow

        tournament_manager = TournamentManager(TournamentManagerConfiguration(self.players))
        result = tournament_manager.run_tournament()
        result = self.__reformat_tournament_result(result)
        self.notify_tournament_end(result)
        pprint(result)
        self.__reset()
        return self.start()

    
    def __reformat_tournament_result(self, result):
        def modify(misbehavors, meet_up):
            meet_up = list(map(lambda p: p.replace('b\'', ''), meet_up))
            meet_up = list(map(lambda p: p.replace('\'', ''), meet_up))
            meet_up = list(map(lambda p: p.replace('"', ''), meet_up))

            loser = meet_up[1]
            if loser in misbehavors:
                return meet_up + ["irregular"]
            return meet_up

        return list(map(lambda m: modify(result[0], m), result[1]))
        


    def notify_tournament_end(self, result):
        for p in self.players:
            p.game_over(result)


    def __accept_connections(self):
        """
        Accept incoming TCP connections and delegating each one
        to a new thread to handle player initialization.
        """

        @timeout(self.waiting_for)
        def go():
            while True:
                conn, addr = self.__socket.accept()
                thread = Thread(target=self.__init_player, args=(conn,))
                thread.start()

        try:
            go()
        except TimeoutError:
            return
            
        
    def __init_player(self, connection):
        """
        Create a RemotePlayer from the TCP connection and append to players list.

        :param connection: conn, TCP connection
        """
        name = connection.recv(self.buffer_size)
        player = RemotePlayer(str(name), connection)
        self.players.append(player)


    def close(self):
        self.__socket.close()


if __name__ == "__main__":
    server = XServer()
    server.start()