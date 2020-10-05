"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow 5 pending connects

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    time.sleep(5)                                # simulate a blocking activity
    while True:                                  # read, write a client socket

        #work done by thread
        data = connection.recv(4096)
        if not data: break
        string = data.decode()

        #seperate word input and number input in a list
        string = string.split()

        #handle start and end of input by getting location of wildcard
        location = string[0].index("*")
        #before (not including) wildcard
        first_part = string[0][:location]
        #after (not including) wildcard
        last_part = string[0][location + 1:]
        length_input = len(string[0])


        #get words from text file to compare
        f = open("Wordlist.txt", "r")
        #better implementation have the open inside a try for error handling
        Words = []
        #put words into a list 
        for (cnt, line) in enumerate(f):
            Words.append(str(line).strip())
        #done dealing with file so close
        f.close()

        #handle number of letters in wild card location
        #get number from input
        input_number = int(string[1]) 
        matched_words = "The matches are:"
        print("checking matches!")

        #check every word in Wordlist.txt
        for word in Words:
            #if wild card is first char and there is a last_part to compare
            if location == 0 and len(last_part) > 0:
                #check if the last_part matches
                if last_part == word[-(len(last_part)):]:
                    ##check if length of wild card fits within constraint of input (<= input_number)
                    if len(word) - length_input < input_number:
                        matched_words += ", " + word
                        continue
                    else:
                        continue
                else:
                    continue

            #if wildcard is inbetween first and last char
            elif len(first_part) > 0 and len(last_part) > 0:
                #check if before and after wild card match
                if first_part == word[:location] and last_part == word[-(len(last_part)):]:
                    
                    #check if length of wild card fits within input (<= input)
                    if len(word) - length_input < input_number:
                        matched_words += ", " + word
                        continue
                    else:
                        continue
                else:
                    continue
            
            #if wildcard is last char and there is first_part to compare
            elif location == length_input - 1 and len(first_part) > 0:
                #check if the first_part matches
                if first_part == word[:location]:
                    ##check if length of wild card fits within input (<= input)
                    if len(word) - length_input < input_number:
                        matched_words += ", " + word
                        continue
                    else:
                        continue
                else:
                    continue
            else:
                continue
        
        
        #send matched_words to client
        connection.send(matched_words.encode())

        connection.send("\n All done!".encode())

        print("matches returned!")


        #none = "done"
        #reply = 'Echo=>%s at %s' % (none, now())

    connection.close()

def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        #connection is new socket created to communicate with the respective socket 
        connection, address = sockobj.accept()   # pass to single-thread for service
        print('Server connected by', address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient, (connection,))

dispatcher()
