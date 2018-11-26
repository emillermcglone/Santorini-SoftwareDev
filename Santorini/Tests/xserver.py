"""
XServer starts up a Santorini game server that hosts a tournament among remote players 
through TCP connections. 
"""

import sys
sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')

from Admin.server_configurations.stdin_server_configuration import ServerConfiguration

class XServer:
    """ Server to host Santorini game among remote players connected through TCP. """

    def __init__(self, configuration=ServerConfiguration()):
        """
        Initialize XServer with server configuration.

        :param configuration: ServerConfiguration, server configuration
        """
        self.min_players = configuration.min_players()
        self.port = configuration.port()
        self.waiting_for = configuration.waiting_for()
        self.repeat = configuration.repeat()
        
        
