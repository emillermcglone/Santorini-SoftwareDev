import socket
import sys
import fileinput
import json

from splitstream import splitfile

HOST, PORT = "localhost", 8000
BUFFER_SIZE = 1024

def connect():
    """ Create and return socket connection instance to server """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def send(msg):
    """ Send msg to the server and return reply """
    sock = connect()
    recv_data = ""
    data = True

    sock.sendall(msg.encode())

    while data:
        data = sock.recv(BUFFER_SIZE).decode()
        if data == True:
                break
        recv_data += data

    sock.close()
    return recv_data


def main():
    internal_name = send("cs4500")


if __name__ == "__main__":
    main()
