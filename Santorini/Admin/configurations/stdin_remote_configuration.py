import json, fileinput, sys
sys.path.append(sys.path[0] + "/../../")

from Lib.util import import_cls
from Admin.configurations.stdin_configuration import STDINConfiguration

class STDINRemoteConfiguration(STDINConfiguration):
    """
    Configuration that extracts players and observers from stdin JSON values. 
    """
    
    def __init__(self):
        """
        initialize the configuration
        """
        self.configuration = None

    def ip(self):
        try:
            self._set_configuration()
            ip = self.configuration['ip']

            if not isinstance(ip, str):
                raise Exception()

            return ip

        except:
            print("No valid configuration found. Try again")
            sys.exit()

    def port(self):
        try:
            self._set_configuration()
            port = self.configuration['port']

            if not self.__valid_port(port):
                raise Exception()

            return port

        except:
            print("No valid configuration found. Try again")
            sys.exit()



    def __valid_port(self, value):
        """
        Is given port number valid?

        :param value: Any, value to check
        :return bool, True if valid port number, False otherwise
        """
        return self.__natural(value) and value >= 50000 and value <= 60000


    def __natural(self, value):
        """ 
        Is given value a natural number?

        :param value: Any, value to check
        :return: bool, True if natural number, False otherwise
        """
        return not isinstance(value, bool) and isinstance(value, int) and value >= 0

