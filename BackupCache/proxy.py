import socket, sys
import time

class fileproxy:
    def __init__(self, port, conn=None):
        if conn == None:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(('localhost', port))
            self.cache = {}
        else:
            self.conn = conn
    def read(self, filename):
        if filename in self.cache:
            print "File Returned from Cache\n"
            return self.cache[filename]
        else:
            message = "Read : " + filename
            self.conn.send(message)
            data = self.conn.recv(1024)
            self.cache[filename] = data
            return(data)
    def write(self, filename, file):
        self.conn.send("Write : "+filename)
        self.conn.send("Write : "+str(len(file)))
        self.conn.send(file)
        self.cache[filename] = file
