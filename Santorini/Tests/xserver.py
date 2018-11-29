"""
XServer starts up a Santorini game server that hosts a tournament among remote players 
through TCP connections. 
"""

import sys
import socket
import json
import names
import fileinput
import names

sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from threading import Thread
from timeout_decorator import timeout, TimeoutError
from pprint import pprint

from Admin.server_configurations.stdin_server_configuration import ServerConfiguration
from Admin.tournament_manager import TournamentManager
from Admin.configurations.standard_configuration import StandardConfiguration
from Remote.remote_player import RemotePlayer


class XServer:
    """ Server to host Santorini game among remote players connected through TCP. """

    def __init__(self, configuration=ServerConfiguration()):
        """
        Initialize XServer with server configuration.

        :param configuration: ServerConfiguration, server configuration
        """
        # Server attributes
        self.ip = 'localhost'
        self.buffer_size = 1024

        # Configuration attributes
        self.min_players = configuration.min_players()
        self.port = configuration.port()
        self.waiting_for = configuration.waiting_for()
        self.repeat = configuration.repeat()
        
        # Socket initialization
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.ip, self.port))

        # Remote players connected
        self.players = []


    def start(self):
        """
        Start server and spin up a new thread for it. If there's not enough
        players, reset server if repeating, exit program otherwise. 
        """

        # Start socket
        self.__socket.listen(3)
        self.live = True

        # Accept all connections
        self.__accept_connections()

        # Reset in case of insufficient players
        if len(self.players) < self.min_players:
            self.__reset()
            return self.start() # return to avoid stack overflow

        # Run TournamentManager
        tournament_manager = TournamentManager(StandardConfiguration(self.players, []))
        result = tournament_manager.run_tournament()

        # Print result and notify players
        result = self.__reformat_tournament_result(result)
        self.notify_tournament_end(result)
        print(json.dumps(result))

        # Reset and start again
        self.__reset()
        self.start()

    
    def __reformat_tournament_result(self, result):
        """
        Given result from TournamentManager, reformat it to Results.

        :param result: [[string, ...], [[string, string], ...]], results from TournamentManager
        :return: Results, reformatted results
        """
        def modify(misbehavors, meet_up):
            loser = meet_up[1]
            if loser in misbehavors:
                return meet_up + ["irregular"]
            return meet_up

        return list(map(lambda m: modify(result[0], m), result[1]))
        


    def notify_tournament_end(self, result):
        """
        Notify players of end of tournament.

        :param result: Results, results of tournament
        """
        for p in self.players:
            p.tournament_end(result)


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
        name = connection.recv(self.buffer_size).decode()
        player = RemotePlayer(json.loads(name), connection)
        self.players.append(player)


    def __reset(self):
        """
        Reset the server after a tournament has ended or when not enough players connect.
        Players are disconnected and emptied. 
        """
        for p in self.players:
            p.disconnect()

        self.players = []

        if not self.repeat:
            self.close()
            sys.exit()


    def close(self):
        """ Close the socket """
        self.__socket.close()


if __name__ == "__main__":
    server = XServer()
    server.start()