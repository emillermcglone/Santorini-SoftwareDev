import socket, sys
from threading import Thread

sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from Admin.configurations.stdin_remote_configuration import STDINRemoteConfiguration
from Remote.proxy import ClientProxy
from Remote.proxy_player import ProxyPlayer


class XClients:
    """
    Client side of a Santorini tournament for a configuration.
    """

    def __init__(self, configuration=STDINRemoteConfiguration()):
        """
        Initialize XClients with given configuration. 

        :param configuration: Configuration, configuration for xclients.
        """
        self.players = configuration.players()
        self.observers = configuration.observers()
        self.ip = configuration.ip()
        self.port = configuration.port()

        self.proxy_players = list(map(lambda p: ProxyPlayer(p, self.__make_proxy()), self.players))


    def run(self):
        """
        Run client side Santorini for each ProxyPlayer.
        """
        for p in self.proxy_players:
            thread = Thread(target=p.run)
            thread.start()


    def __make_proxy(self):
        """
        Make a new ClientProxy with ip address and port number.

        :return: ClientProxy, client proxy
        """
        return ClientProxy(self.ip, self.port)


if __name__ == "__main__":
    xclients = XClients()
    xclients.run()
