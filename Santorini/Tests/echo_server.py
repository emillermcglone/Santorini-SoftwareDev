import socket
import threading


class EchoServer:
    def __init__(self, ip, port, holder, buffer_size = 1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.holder = holder
        self.live = False


    def start(self):
        if self.live:
            return

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.ip, self.port))
        self.__socket.listen(3)
        self.live = True

        thread = threading.Thread(target=self.__serve)
        thread.start()


    def __serve(self):
        while True:
            conn, addr = self.__socket.accept()
            thread = threading.Thread(target=self.__serve_connection, args=(conn,))
            thread.start()


    def __serve_connection(self, conn):
        while self.live:
            response = conn.recv(self.buffer_size)
            conn.sendall(response)
            self.holder.update(response.decode())


    def close(self):
        self.__socket.close()
        self.live = False

