#!/usr/bin/env python

import socket
import importlib
import sys

import io

sys.path.append('../2/Aux')
two = __import__('2')

TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

connection, address = s.accept()
while True:
    data = connection.recv(BUFFER_SIZE).decode('utf-8')
    if not data: break
    io_buffer = io.StringIO(data)
    connection.send(two.format_json_inputs(io_buffer).encode('utf-8'))
connection.close()