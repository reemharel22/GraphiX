import socket
from asyncore import *

#For connections:
class Handler(dispatcher):
    def __init__(self, socket, asyncon):
        dispatcher.__init__(self, socket)
        self.asyncon = asyncon

    def handle_read(self):
        self.asyncon.msg = self.recv(4096)


class AsyncConn(dispatcher):
    def __init__(self, port=12355):
        print port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        dispatcher.__init__(self)
        self.set_socket(s)
        self.msg = ""
        self.accepted = False
        self.bind(('127.0.0.1', port))
        self.listen(5)
        self.set_reuse_addr()

    def handle_read(self):
        print "reading"
        data = self.recv(1024)
        if data:
            print data

    def handle_write(self):
        pass

    def readable(self):
        return True

    def handle_accept(self):
        self.accepted = True
        socket, addr = self.accept()
        Handler(socket, self)

#Static functions: