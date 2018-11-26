"""
XServer starts up a Santorini game server that hosts a tournament among remote players 
through TCP connections. 
"""

import sys
import socket

from threading import Thread
from timeout_decorator import timeout, TimeoutError

sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from Admin.server_configurations.stdin_server_configuration import ServerConfiguration
from Admin.tournament_manager import TournamentManager
from Player.players.remote_player import RemotePlayer


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


    def start(self):
        """
        Start server and spin up a new thread for it. 
        """
        self.__socket.listen(3)
        self.live = True

        thread = Thread(target=self.__accept_connections)
        thread.start()


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
        player = RemotePlayer(name, connection)
        self.players.append(player)


    def close(self):
        pass