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
        if data == True: break
        recv_data += data

    sock.close()
    return recv_data

def get_json_inputs(source):
    """ Get json inputs from source """
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
        for i in get_json_inputs(source):
            json_inputs.append(i)
            if i[0] == "at":
                output.write(send('\n'.join(list(map(lambda x: str(x), json_inputs)))))
                json_inputs = []

if __name__ == "__main__":
    main(sys.stdin, sys.stdout)
