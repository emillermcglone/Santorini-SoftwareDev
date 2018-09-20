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


def send(message):
    """ 
    Send message to the server and return reply.
    
    @param message: Message string sent to server
    @return: Response in utf-8 received from server
    """
    sock = connect()
    recv_data = ""
    data = True

    sock.sendall(message.encode())

    while data:
        data = sock.recv(BUFFER_SIZE).decode()
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


def main(source, output):
    internal_name = send("cs4500")
    json_inputs = []

    while True:
        current_inputs = get_json_inputs(source)
        for j in current_inputs:
            json_inputs.append(j)
            if isinstance(j, list) and j[0] == "at":
                str_json_inputs = list(map(str, json_inputs))
                output.write(send("\n".join(str_json_inputs)))
                json_inputs = []


if __name__ == "__main__":
    try:
        source = open(sys.argv[1])
    except:
        source = sys.stdin
    main(source, sys.stdout)
