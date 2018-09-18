import socketserver
import sys
from contextlib import redirect_stdout
from io import StringIO
from importlib.machinery import SourceFileLoader

twoFile = SourceFileLoader("2.py", "../../2/Aux/2.py").load_module()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        this is the main function for the MyTCPHandler module
        it handles requests one at a time
        """
        self.data = self.request.recv(1024).rstrip()
        rawJSON = self.data.decode('utf-8')

        jsonList = rawJSON.splitlines()

        # redirect stdout of 2.py to stream
        stream = StringIO()
        stream_redirect = redirect_stdout(stream)
        try:
            with stream_redirect:
                jsonController = twoFile.Controller()
                jsonController.run(1, jsonList)
        except ValueError:
            pass
        
        self.request.sendall(bytes(stream.getvalue(), "utf-8"))

        

if __name__ == "__main__":
    host, port = "localhost", 8000
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            exit(0)
