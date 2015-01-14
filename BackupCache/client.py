import socket, sys
import time
import proxy

PORT = int(sys.argv[1]) # Arbitrary non-privileged port
reader = proxy.fileproxy(PORT)

while True:
	validinput = False
	while validinput is False:
		message = raw_input("Press w to write a message and r to read one\n")
		if (message == 'w') or (message == 'r'):
			validinput = True
	filename = raw_input("name the file\n")
	if message == 'r':
		print(reader.read(filename))
	else:
		file = raw_input("Type in the file\n")
		reader.write(filename, file)
