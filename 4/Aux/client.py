import socket
import sys
import fileinput
import json

from splitstream import splitfile


def connect(host, port):
    """ 
    Create and return socket connection instance to server

    @param host: the IP address for server
    @param port: the port number to connect to 
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def send(sock, message):
    """
    Send message to the server and return reply.

    @param host: the IP address for server
    @param port: the port number to connect to
    @param message: Message string sent to server
    @return: Response in utf-8 received from server
    """
    recv_data = ""
    sock.send(message.encode())
    return sock.recv(1024).decode()


def get_json_inputs(source):
    """
    Get json inputs from source

    @param source: Source with 'read' attribute for json inputs
    @return: list of extracted json inputs
    """
    json_inputs = []
    for line in splitfile(source, format="json"):
        try:
            json_inputs.append(json.loads(line))
        except:
            continue
    return json_inputs


def is_named_request(json_value):
    if not isinstance(json_value, list):
        return False

    return len(json_value) == 3 and json_value[0] == "sheet" and isinstance(json_value[1], str) and isinstance(json_value[2], list) and all(isinstance(x, list) for x in json_value[2])

def is_set_request(json_value):
    if not isinstance(json_valuem, list):
        return False

    return len(json_value) == 5 and json_value[0] == "set" and isinstance(json_value[1], str)


def establish_connection(host, port, source, output):
    sock = connect(host, port)
    internal_name = send(sock, "\"gija-emmi\"")
    json_inputs = []

    print(host)

    while True:
        current_inputs = get_json_inputs(source)
        for j in current_inputs:
            json_inputs.append(j)
            if isinstance(j, list) and j[0] == "at":
                message = str(json_inputs)
                print(message)
                output.write(send(sock, message))
                json_inputs = []


def is_file_found(path):
    """
    Check if given path to file exists

    @param path: path to file
    @return: True if exists, False otherwise
    """
    try:
        file = open(path)
        file.close()
        return True
    except:
        return False


def main():
    """
    Get command line arguments for host IP address and source of inputs.
    First argument is IP address, second is file path. First argument is
    file path if IP address is not given. These are optional arguments.
    IP address defaults to 'localhost' and source to 'sys.stdin'.
    """
    host, port = sys.argv[1], 8000
    source = sys.stdin

    if len(sys.argv) >= 3:
        source = open(sys.argv[2]) if is_file_found(sys.argv[2]) else sys.stdin
        if is_file_found(sys.argv[1]):
            source = open(sys.argv[1])

    establish_connection(host, port, source, sys.stdout)


if __name__ == "__main__":
    main()
