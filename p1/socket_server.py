import socket
from datetime import datetime

# Function to calculate the expression
def calculate_expression(expression):
    # TODO: Implement this function
    result = 0
    sp = str(expression)
    if "+" in sp:
        operation = str('+')
        op = sp.split('+')
    elif "-" in sp:
        operation = str("-")
        op = sp.split('-')
    elif "*" in sp:
        operation = str("*")
        op = sp.split('*')
    elif "/" in sp:
        operation = str("/")
        op = sp.split('/')
    elif "^" in sp:
        operation = str("^")
        op = sp.split('^')
    elif "%" in sp:
        operation = str("%")
        op = sp.split('%')
    elif "=" in sp:
        operation = str("=")
        op = sp.split('=')
    elif ">" in sp:
        operation = str(">")
        op = sp.split('>')
    elif "<" in sp:
        operation = str("<")
        op = sp.split('<')
    else:
        pass
    # +|-|*|/|^|%|=|>|<
    left_or = op[0]
    right_or = op[1] 

    left = int(left_or)
    right = int(right_or)
        

    if operation == "+":
        result = left + right

    elif operation == "-":
        result = left - right

    elif operation == "*":
        result = left * right

    elif operation == "/" :
        result = left / right

    elif operation == "^" :
        result = 1
        for i in range(right):
            result = result * left

    elif operation == "%" :
        result = left % right

    elif operation == "=" :
        if left == right:
            result = 1
        else:
            result = 0

    elif operation == ">" :
        if left > right:
            result = 1
        else:
            result = 0

    elif operation == "<" :
        if left < right:
            result = 1
        else:
            result = 0
    else:
        pass
    
    return str(float(result))

# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
HOST = "127.0.0.1"
PORT = 2174
# TODO end

with open('./server_log.txt', 'w') as logFile:
    # 1. Create a socket
    # 2. Bind the socket to the address
    # TODO Start
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST,PORT))
    # TODO End

    while True:
        # Listen to a new request with the socket
        # TODO Start
        serverSocket.listen(1)
        # TODO End

        now = datetime.now()
        print("The Server is running..")
        logFile.write(now.strftime("%H:%M:%S ") + "The Server is running..\n")
        logFile.flush()


        # Accept a new request and admit the connection
        # TODO Start
        client, address = serverSocket.accept()
        # TODO End

        client.settimeout(15)
        print(str(address) + " connected")
        now = datetime.now()
        logFile.write(now.strftime("%H:%M:%S ") + "connected " + str(address) + '\n')
        logFile.flush()

        try:
            while True:
                client.send(b"Please input a question for calculation")

                # Recieve the data from the client
                # TODO Start
                question = client.recv(1024).decode()
                # TODO End

                now = datetime.now()
                logFile.write(now.strftime("%H:%M:%S ") + question + '\n')
                logFile.flush()

                # TODO: Call the calculate_expression function here
                ans = calculate_expression(question)

                # Ask if the client want to terminate the process
                message = f"{ans}\nDo you wish to continue? (Y/N)"


                # Send the answer back to the client
                # TODO Start
                client.send(message.encode())
                # TODO End
                
                # Terminate the process or continue
                check = client.recv(1024).decode()
                if check.lower() != 'y':
                    break
        except ConnectionResetError:
            print("Connection reset by peer")
            logFile.write("Connection reset by peer\n")
            logFile.flush()
        except Exception as e:
            print("An error occurred:", e)
            logFile.write(f"An error occurred: {e}\n")
            logFile.flush()

        client.close()

logFile.close()
