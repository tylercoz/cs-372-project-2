"""
Author: Tyler Cozzocrea
Purpose: CS 372
Description: Connect to an internet domain and send it a basic request
             it's root directory. Add domain such as "google.com" after
             calling script.
             EX:
                 > python3 webclient.py google.com
"""
import sys
import socket

if len(sys.argv) != 2:
    print("Please enter exactly one argument into the script.")
    print("Usage:\n\tpython3 webclient.py [web server address]")
    quit()

mySocket = socket.socket()

web_address = sys.argv[1]
port = 80
mySocket.connect((web_address, port))

request = "GET / HTTP/1.1\r\n\
Host: example.com\r\n\
Connection: close\r\n\
\r\n"
mySocket.sendall(request.encode("ISO-8859-1"))

response = b''
while (incoming_data := mySocket.recv(1)) != b'':
    response += incoming_data
response = response.decode("ISO-8859-1")
print(response)

mySocket.close()
