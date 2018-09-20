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


def send(host, port, message):
    """
    Send message to the server and return reply.

    @param host: the IP address for server
    @param port: the port number to connect to
    @param message: Message string sent to server
    @return: Response in utf-8 received from server
    """
    sock = connect(host, port)
    recv_data = ""
    data = True

    sock.sendall(message.encode())

    while data:
        data = sock.recv(1024).decode()
        if data == True:
            break
        recv_data += data

    sock.close()
    return recv_data


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


def establish_connection(host, port, source, output):
    internal_name = send(host, port, "cs4500")
    json_inputs = []

    while True:
        current_inputs = get_json_inputs(source)
        for j in current_inputs:
            json_inputs.append(j)
            if isinstance(j, list) and j[0] == "at":
                str_json_inputs = list(map(str, json_inputs))
                output.write(send(host, port, "\n".join(str_json_inputs)))
                json_inputs = []

def is_ip_address(address):
    """
    Check if given string is valid IP address

    @param address: string IP address
    @return: True if valid, False otherwise
    """
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

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
    host, port = "localhost", 8000
    source = sys.stdin

    if len(sys.argv) == 2:
        if is_ip_address(sys.argv[1]):
            host = sys.argv[1]
        elif is_file_found(sys.argv[1]):
            source = open(sys.argv[1])
    elif len(sys.argv) >= 3:
        if is_ip_address(sys.argv[1]):
            host = sys.argv[1]
            source = open(sys.argv[2]) if is_file_found(sys.argv[2]) else sys.stdin
        elif is_file_found(sys.argv[1]):
            source = open(sys.argv[1])
            
    establish_connection(host, port, source, sys.stdout)

if __name__ == "__main__":
    main()