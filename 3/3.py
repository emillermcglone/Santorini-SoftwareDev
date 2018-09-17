#!/usr/bin/env python

import socketserver
import importlib
import io
import sys

sys.path.append('../2/Aux')
two = __import__('2')

class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        json_inputs = self.data.decode('utf-8')
        io_buffer = io.StringIO(json_inputs)

        # send back JSON values with reverse positions
        self.request.sendall(two.format_json_inputs(io_buffer).encode('utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        # Activate the server; this will keep running until interrupted with Ctrl-C
        server.serve_forever()
