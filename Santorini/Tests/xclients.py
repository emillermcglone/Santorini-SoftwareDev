"""
XClients runs the client side of a Santorini game server. It configures itself with the 
player components and connect them to the server. 
"""

import sys
import socket
import json
import fileinput
import time

from threading import Thread
from timeout_decorator import timeout, TimeoutError

# Access to all modules
sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from Admin.configurations.stdin_remote_configuration import STDINRemoteConfiguration
from Remote.relay import Relay
from Remote.relay_player import RelayPlayer


class XClients:
    """ Client side of a Santorini tournament. """

    def __init__(self, configuration=STDINRemoteConfiguration()):
        """
        Initialize XClients with given configuration, which provides, players, observers, ip
        address and port number.

        :param configuration: Configuration, configuration for xclients.
        """
        self.players = configuration.players()
        self.observers = configuration.observers()
        self.ip = configuration.ip()
        self.port = configuration.port()

        self.relay_players = list(map(lambda p: RelayPlayer(p, self.__make_proxy()), self.players))


    def run(self):
        """
        Run client side Santorini and spin up a new thread for each RelayPlayer.
        """
        threads = []
        for p in self.relay_players:
            thread = Thread(target=p.run)
            thread.start()
            threads.append(thread)
            time.sleep(1)

        for thread in threads:
            thread.join()

        sys.exit()
        
            

    def __make_proxy(self):
        """
        Make a new Relay with ip address and port number.

        :return: Relay, client proxy
        """
        return Relay(self.ip, self.port)



if __name__ == "__main__":
    xclients = XClients()
    xclients.run()
