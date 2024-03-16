import socket
import sys

import re

# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
HOST = '127.0.0.1'
PORT = 2174
# TODO end


# 1. Create a socket
# 2. Bind the socket to the address
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST,PORT)) 
# TODO End

# Listen for incoming connections (maximum of 1 connection in the queue)
# TODO Start
serverSocket.listen(10)
# TODO End

# Start an infinite loop to handle incoming client requests
while True:
    print('Ready to serve...')

    # Accept an incoming connection and get the client's address
    # TODO Start
    connectionSocket, address = serverSocket.accept()
    # TODO End
    print(str(address) + " connected")

    try:
        # Receive and decode the client's request
        # TODO Start
        message = connectionSocket.recv(4096).decode()
        # print(message)
        # TODO End

        # If the message is empty, set it to a default value
        if message == "":
            message = "/ /"

        # Print the client's request message
        print(f"client's request message: \n {message}")

        # Extract the filename from the client's request
        # TODO Start
        filename = str(message.split()[1])
        filename = filename.replace("/","")
        # filename = re.split(r'[ /, ]', message)[2]
        # TODO End
        print(f"Extract the filename: {filename}")

        if filename != 'index.html' and filename !='helloworld.html':
            connectionSocket.send('HTTP/1.1 404 NotFound\r\n'.encode())
            connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not found</h1></body></html>\r\n".encode())
            connectionSocket.close()
            continue

        # Open the requested file
        # Read the file's content and store it in a list of lines
        f = open(filename)
        out_put_data = f.readlines()
        f.close()

        # 1. Send an HTTP response header to the client
        # 2. Send the content of the requested file to the client line by line
        # 3. Close the connection to the client
        # TODO Start
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())

        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        for line in out_put_data:
            connectionSocket.send(line.encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
        # TODO End

    except IOError:
        # If the requested file is not found, send a 404 Not Found response
        # TODO Start
        # connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())
        connectionSocket.send("HTTP/1.1 404 Not found\r\n".encode())
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not found</h1></body></html>\r\n".encode())
        connectionSocket.close()
        # TODO End
