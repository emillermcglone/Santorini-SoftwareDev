"""
Client side TCP connection module for Players to connect to
tournament manager and referee on a Santorini game server.
"""

import socket
from threading import Thread

class ClientProxy:
    """ Proxy to connect to a remote server through TCP. """

    def __init__(self, ip, port, buffer_size = 1024):
        """
        Initialize Proxy and connect to IP address at given port automatically.

        :param ip: string, IP address to connect to
        :param port: int, port number
        :param buffer_size: int, byte size for data transfer
        """
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size

        self.__live = False


    @property
    def live(self):
        """
        Is proxy connection live?

        :return: bool, True if live, False otherwise
        """
        return self.__live

    
    def connect(self):
        """ Connect to IP address at port if connection isn't live already. """
        if self.__live:
            return

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.ip, self.port))
        self.__live = True


    def subscribe(self, subscriber, connection_loss_handler):
        """
        Subscribe subscriber to socket connection.

        :param subscriber: (string) -> void, function that handles messages from socket
        :param connection_loss_handler: () -> void, function that handles connection close or loss
        """
        self.connect()
        thread = Thread(target=self.__run_subscription, args=(subscriber, connection_loss_handler))
        thread.start()


    def __run_subscription(self, handler, connection_loss_handler):
        """
        Run the subscription for given handler.

        :param handler: (string) -> void, function that handles messages from socket
        """
        while self.__live:
            data = self.receive()                
            handler(data)
        
        connection_loss_handler()


    def send(self, message):
        """
        Send message to the socket.

        :param message: string, message to send 
        :return: string, message from socket
        """
        self.connect()
        message = message.encode()

        try:
            self.__socket.sendall(message)
        except ConnectionError:
            self.__live = False

    
    def receive(self):
        """
        Receive message from the socket.

        :return: string, message from socket
        """
        self.connect()

        try:
            return self.__socket.recv(self.buffer_size).decode()
        except ConnectionError:
            self.__live = False


    def close(self):
        """
        Close the socket connection if it's live.
        """
        if not self.__live:
            return

        self.__socket.close()
        self.__live = False
