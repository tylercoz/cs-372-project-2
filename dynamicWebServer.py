"""
Author: Tyler Cozzocrea
Purpose: CS 372
Description: Create a basic web server.
             EX:
                 > python3 webserver.py 15000
"""

import socket
import sys
import os

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
    return request.decode("ISO-8859-1")

def root_response():
    header = ""
    header += "HTTP/1.1 200 OK\r\n"
    header += "Content-Type: text/plain\r\n"
    header += "Content-Length: 27\r\n"
    header += "Connection: close\r\n"
    header += "\r\n"
    header += "This is the root directory."
    return header

def send_404(connection):
    response = ""
    response += "HTTP/1.1 404 File Not Found\r\n"
    response += "Content-Type: text/plain\r\n"
    response += "Content-Length: 13\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += "404 not found"

    connection.sendall(response.encode("ISO-8859-1"))

def get_file_path(request):
    first_line_of_request = request.split('\r\n')[0]
    file_path = first_line_of_request.split()[1]
    return file_path

def get_file_name(path):
    return os.path.split(path)[-1]


def get_file_data(file_name):
    with open(file_name, "rb") as fp:
        data = fp.read()   # Read entire file
        return data

    raise FileNotFoundError


def parse_request(request):
    file_attributes = {}
    file_attributes['path'] = get_file_path(request)
    if file_attributes['path'] == "/":
        return file_attributes
    file_attributes['name'] = get_file_name(file_attributes['path'])
    file_attributes['type'] = os.path.splitext(file_attributes['name'])[-1]

    data = get_file_data(file_attributes['name'])
    if isinstance(data, bytes):
        file_attributes['data'] = data
        file_attributes['len'] = len(data)

    return file_attributes

def build_response(file_attributes):
    if file_attributes['path'] == "/":
        return root_response()

    header = ""
    header += "HTTP/1.1 200 OK\r\n"
    if file_attributes['type'] == ".html":
        header += "Content-Type: text/html\r\n"
    else:
        header += "Content-Type: text/plain\r\n"
    header += f"Content-Length: {file_attributes['len']}\r\n"
    header += "Connection: close\r\n"
    header += "\r\n"
    header += f"{file_attributes['data']}"
    return header

def send_response(connection, request):
    try:
        request_attributes = parse_request(request)
    except FileNotFoundError:
        send_404(connection)
        return

    response = build_response(request_attributes)
    connection.sendall(response.encode("ISO-8859-1"))

def main():

    if not command_line_argument_exists():
        print("Please enter exactly one argument into the script.")
        print("Usage:\n\tpython3 webserver.py [port number]")
        quit()

    listening_socket = create_listening_socket(sys.argv[1])

    while True:
        connection, client_address = listening_socket.accept()
        print(f"Accepting connection on {client_address}")

        request = get_request(connection)
        send_response(connection, request)

        print(f"Closing connection on {client_address}\n")
        connection.close()

if __name__ == "__main__":
    main()
