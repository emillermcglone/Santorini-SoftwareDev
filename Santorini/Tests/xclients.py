import socket

from Admin.configurations.stdin_remote_configuration import STDINRemoteConfiguration
from Remote.proxy import ClientProxy


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

        self.proxy = ClientProxy(self.ip, self.port)
        


    def run(self):
        pass

    
