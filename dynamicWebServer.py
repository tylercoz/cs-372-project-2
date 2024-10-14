"""
Author: Tyler Cozzocrea
Purpose: CS 372
Description: Create a basic web server.
             EX:
                 > python3 webserver.py 15000
"""
import socket
import sys

if len(sys.argv) != 2:
    print("Please enter exactly one argument into the script.")
    print("Usage:\n\tpython3 webserver.py [port number]")
    quit()

port = sys.argv[1]
listening_socket = socket.socket()
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listening_socket.bind(('', int(port)))

print(f"Listening for connections on port {port} ...")
listening_socket.listen()

while True:
    connection, client_address = listening_socket.accept()
    print(f"Accepting connection on {client_address}")
    request = b''
    while True:
        incoming_data = connection.recv(64)
        request += incoming_data
        request_literal = request.decode("ISO-8859-1")
        if request_literal[-4:] == '\r\n\r\n':
            break

    response = "HTTP/1.1 200 OK\r\n\
Content-Type: text/plain\r\n\
Content-Length: 6\r\n\
Connection: close\r\n\
\r\n\
Hello!"

    connection.sendall(response.encode("ISO-8859-1"))
    print(f"Closing connection on {client_address}\n")
    connection.close()
