"""
Author: Tyler Cozzocrea
Purpose: CS 372
Description: Create a basic web server.
             EX:
                 > python3 webserver.py 15000
"""

"""
SCRATCH
- [ ] Parse that request header to get the file name.
- [ ] Strip the path off for security reasons.
- [ ] Read the data from the named file.
- [ ] Determine the type of data in the file, HTML or text.
- [ ] Build an HTTP response packet with the file data in the payload.
- [ ] Send that HTTP response back to the client.

"""
import socket
import sys
def command_line_argument_exists():
    return len(sys.argv) == 2

def create_listening_socket(port):
    listening_socket = socket.socket()
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(('', int(port)))

    print(f"Listening for connections on port {port} ...")
    listening_socket.listen()

    return listening_socket

def get_request(socket):
    request = b''
    while True:
        incoming_data = socket.recv(64)
        request += incoming_data
        request_literal = request.decode("ISO-8859-1")
        if request_literal[-4:] == '\r\n\r\n':
            break
    return request

def create_response():
    response = ""
    response += "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/plain\r\n"
    response += "Content-Length: 6\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += "Hello!"
    return response


if not command_line_argument_exists():
    print("Please enter exactly one argument into the script.")
    print("Usage:\n\tpython3 webserver.py [port number]")
    quit()

listening_socket = createListeningSocket(sys.argv[1])

while True:
    connection, client_address = listening_socket.accept()
    print(f"Accepting connection on {client_address}")

    request = getRequest(connection)
    response = createResponse()
    connection.sendall(response.encode("ISO-8859-1"))
    print(f"Closing connection on {client_address}\n")
    connection.close()
