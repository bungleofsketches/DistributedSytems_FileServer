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
            port = self.what_server(filename)
            tempconn = self.new_connection(port)
            message = "Read : " + filename
            tempconn.send(message)
            data = tempconn.recv(1024)
            self.cache[filename] = data
            return(data)

    def write(self, filename, file):
        port = self.what_server(filename)
        tempconn = self.new_connection(port)
        print ("Connected\n")
        tempconn.send("Write : "+filename)
        if tempconn.recv(1024) == "Ready":
            tempconn.send("Write : "+str(len(file)))
            if tempconn.recv(1024) == "Ready":
                print ("Write Message Sent\n")
                self.cache[filename] = file
                tempconn.send(file)
                return tempconn.recv(1024)

    def what_server(self, filename):
        self.conn.send("WheresFile : "+ filename)
        port = self.conn.recv(1024)
        if port == "0":
            self.conn.send("WheresNext : ")
            port = self.conn.recv(1024)
        return int(port)

    def new_connection(self, port):
        tempconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempconn.connect(('localhost', int(port)))
        return tempconn
