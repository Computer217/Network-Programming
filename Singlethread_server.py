import time, _thread as thread        
from socket import * 

#any local host
myHost = '' 
#port waiting for client query                         
myPort = 50008

#create a TCP socket // bind it to the server port // allow 1 pending connection
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(1)

def main():
    #simulate the latency in serving real jobs
    #thread that is serving a client waits 5 seconds
    time.sleep(5)

    #server socket always listening
    while True:
        connection, address = sockobj.accept()   # pass to single-thread for service
        print('Server connected by', address, end=' ')
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

        print("matches returned!")


        #none = "done"
        #reply = 'Echo=>%s at %s' % (none, now())

    connection.close()

    #can force the server to close after serving the client by closing server socket
    #else it keeps on listening for clients
    #sockobj.close()
    
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception:
        print("other exception")


