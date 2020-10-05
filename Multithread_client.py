from socket import *
import sys

serverName = 'localhost'
serverPort = 50007

#create client socket to reach the server
#TCP Socket

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    #connect socket to server
    clientSocket.connect((serverName,serverPort))
except OSError as e:
    print ('Unable to connect to socket: ', e)
    if clientSocket:
        clientSocket.close()
        sys.exit(1)


#send word with wild card and number

while True:
    #get 2 inputs from user from stdin
    sentence = input("input word with wild card and number:")

    #if stdin is "quit" then break and close connection with server
    if sentence == "quit":
        break

    #send data through socket
    clientSocket.send(sentence.encode())

    modifiedSentence =""

    while True:

        #no need to attatch port // recieve response from server and print
        modifiedSentence += clientSocket.recv(4096).decode()
        if "\n All done!" in modifiedSentence:
            break

    print ("From Server:", modifiedSentence)

clientSocket.close()

