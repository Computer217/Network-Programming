from socket import *

serverName = 'localhost'
serverPort = 50008

#create client socket 
clientSocket = socket(AF_INET, SOCK_STREAM)

#connect socket to server
clientSocket.connect((serverName,serverPort))

sentence = input("input word with wild card and number:")


#send data through socket
clientSocket.send(sentence.encode())

#no need to attatch port 
modifiedSentence = clientSocket.recv(4096)
print ("From Server:", modifiedSentence.decode())

clientSocket.close()