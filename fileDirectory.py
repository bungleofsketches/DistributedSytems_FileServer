import multiprocessing
import socket, Queue, signal, os.path
import sys
from thread import *

#Function for handling connections. This will be used to create threads
def clientthread(quu, fileservers, files, kill):
    while kill.is_set()==False:
        blocked = True
        while blocked:
            blocked = False
            try:
                connectionTuple = quu.get()
            except Queue.Empty as emp:
                blocked = True
        conn = connectionTuple[0]
        addr = connectionTuple[1]
        print 'Connected to ' + addr[0] + ':' + str(addr[1])
        reply = ""

        while True:
            data = conn.recv(1024)
            if data.startswith("HELO "):
                start = data[5:]
                reply = data+"\nIP:"+str(addr[0])+"\nPort:"+str(PORT)+"\nStudentID:11816252"
            elif data=="KILL_THREAD\n":
                break
            elif data=="KILL_SERVICE\n":
                reply = "panic"
                kill.set()
                sys.exit()
                break
            #Write Notification from Server
            elif data.startswith("Write :"):
                file = parse_rw_line(data)
                serverport = conn.getsockname()
                files[file] = serverport
            #Where Request from Client
            elif data.startswith("WheresFile :"):
                filename = parse_rw_line(data)
                if filename in files:
                    reply = files[filename]
                else:
                    reply = "0"
            elif data.startswith("WheresNext :"):
                reply = fileservers.get()
                fileservers.put(reply)
            elif data.startswith("Register :"):
                port = parse_rw_line(data)
                fileservers.put(port)
                reply = "Registered"
            elif data is None:
                break
            else:
                reply = data.upper()
            conn.send(reply)
        conn.close()

def parse_rw_line(data):
    real_data = ((data.split(" : "))[1]).partition("\r\n")[0]
    return real_data

def write_file(conn, name, lengthAsString):
    path = get_file_path(name)
    length = int(lengthAsString)
    string = conn.recv(length)
    with open(path,'wb') as fname:
        fname.write(string)

def read_file(name):
    path = get_file_path(name)
    with open(path, 'rb') as fname:
        return fname.read()

def get_file_path(name):
    path = os.getcwd() + "/FileStorage/" + name
    return path



###MAIN
HOST = ''
PORT = int(sys.argv[1]) #paramterised port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quu = Queue.Queue()
fileservers = Queue.Queue()
kill = multiprocessing.Event()
files = {}

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed'
    sys.exit()

s.listen(5)
print 'Socket now listening'

for x in range(0, 10):
    start_new_thread(clientthread,(quu, fileservers, files, kill))
while kill.is_set()==False:
    conn, addr = s.accept()
    quu.put((conn,addr))
s.close()
