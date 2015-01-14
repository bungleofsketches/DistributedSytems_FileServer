import sys, os.path

def read_file(name):
    path = get_file_path(name)
    with open(path, 'rb') as fname:
        return fname.read()

def get_file_path(name):
    path = os.getcwd() + "/FileStorage/" + name
    return path

out = read_file("defo.txt")
print(out)
