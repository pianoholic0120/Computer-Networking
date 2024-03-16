import socket
import time
import argparse

# ANSI escape codes for colors
RED = '\033[31m'
RESET = '\033[0m'

def log_message(logFile, message, color=RESET):
    formatted_message = color + message + RESET
    print(formatted_message)
    logFile.write(message + '\n')  # Write the unformatted message to the log file
    logFile.flush()

    
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--server', default="local")
    parser.add_argument('--testcase', default='basic')
    parser.add_argument('--studentID', default= 'b10901151')                    # Modify to your own student ID 
                        
    # Transfer input to dictionary form 
    input_info = vars(parser.parse_args())

    # Set input parameters
    testcase = input_info["testcase"]
    studentID = input_info["studentID"]
    select_server = input_info["server"]
    # select_server = 'TA'
    
    testcase_path = f"./p1_testcase_{testcase}"
    output_path = f"./{studentID}_p1_client_result_{testcase}.txt"

    with open(output_path, 'w') as logFile:
        log_message(logFile, "The Client is running..")

        # Configure the server IP with its corresponding port number
        # Specify the TCP connection type and make connection to the server
        # TODO Start
        if select_server == 'TA':
            HOST = "140.112.42.104"
            PORT = 7777
        else:
            HOST = "127.0.0.1"
            PORT = 2174
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        # TODO End


        # You can change the test case or create other test cases on your own
        with open(testcase_path, 'r') as Testcase:
            for PreprocessingLine in Testcase:
                line = PreprocessingLine.strip()
                time.sleep(3)

                if line == "Y" or line == "N":
                    # If the line is "Y" or "N", treat it as a response to a server prompt
                    response = line
                    log_message(logFile, "Response to server prompt: " + response)

                    # Send the response to the server
                    # TODO Start
                    s.send(response.encode())
                    # TODO End
                else:

                    # Receive the server's message without color
                    # TODO Start
                    server_message = s.recv(1024).decode()
                    # TODO End

                    # Log the server's message
                    log_message(logFile, "Received the message from server: ", RESET)
                    log_message(logFile, server_message, RED)

                    # If not "Y" or "N," assume it's a mathematical expression
                    question = line
                    log_message(logFile, "Question: " + question)

                    # Send the question to the server
                    # TODO Start
                    s.send(question.encode())
                    # TODO End

                    # Receive and log the answer from the server
                    # TODO Start
                    ans = s.recv(1024).decode()
                    # TODO End

                    log_message(logFile, "Get the answer from server: ", RESET)
                    log_message(logFile, ans, RED)

        s.close()
    logFile.close()

if __name__ == '__main__':
    main()
