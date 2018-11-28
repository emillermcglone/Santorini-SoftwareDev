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
from Remote.proxy import ClientProxy
from Remote.proxy_player import ProxyPlayer


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

        self.proxy_players = list(map(lambda p: ProxyPlayer(p, self.__make_proxy()), self.players))


    def run(self):
        """
        Run client side Santorini and spin up a new thread for each ProxyPlayer.
        """
        for p in self.proxy_players:
            thread = Thread(target=p.run)
            thread.start()
            time.sleep(0.5)
            

    def __make_proxy(self):
        """
        Make a new ClientProxy with ip address and port number.

        :return: ClientProxy, client proxy
        """
        return ClientProxy(self.ip, self.port)



if __name__ == "__main__":
    xclients = XClients()
    xclients.run()
