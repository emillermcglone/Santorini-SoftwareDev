"""
Client side TCP connection module for Players to connect to
tournament manager and referee on a Santorini game server.
"""

import socket


class Proxy:
    """
    Proxy for Players to connect to Santorini game server. 
    """

    def __init__(self, ip, port):
        """
        Initialize Proxy and connect to IP address at given port.

        :param ip: string, IP address to connect to
        :param port: int, port number
        """
        self.ip = ip
        self.port = port
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))


    def send(self, message):
        """
        Send message to the socket.

        :param message: string, message to send 
        :return: string, message from socket
        """
        self.socket.send(message.encode())
        return self.receive()

    
    def receive(self):
        """
        Receive message from the socket.

        :return: string, message from socket
        """
        return self.socket.recv(self.buffer_size).decode()


    def close(self):
        """
        Close the socket connection.
        """
        self.socket.close()
