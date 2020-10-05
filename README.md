# Network-Programming
This project focuses on socket programming

Project 1 Design and implementation of a single-thread client / server pair.

Singlethread_client.py
Singlethread_Server.py

More specifically, a server responsible for only serving one client at a time. The single client sends a query to the server; the query consists of an English word with an individual char replaced by “*” representing a wildcard and a number 0-9. The wildcard represents the location in which the input word can vary, and the input number represents the number of max characters that the wildcard represents. 

An example of a valid input would be “zo*e 2”. When the server receives the query, it searches through Wordlist.txt and returns all the words that contain less than or equal to the number input (in this case 2) of chars in place of the wild card. In other words, between the first part of the word input (prefix) and last part of the word input (suffix) (including 0 chars between suffix and prefix).  e.g., assuming these words are in Wordlist.txt, server returns: zoe, zone, zolle. The compiled list by the server is then sent back to the client. 

This functionality is achieved by leveraging a single thread server. Only the main_thread of the program is initialized. I compared the prefix and suffix of each word in the list to the prefix (text before not including *) and suffix (text after * not including) of the input_word. If they matched, check the number of characters in between the prefix and suffix was less than or equal to the number input. If these conditions were satisfied, I added the word to the list being sent to the client after checking every word. Furthermore, I checked for special cases such as if the wild card was the first char or the last char, and if the number input was 0. 

A trade off I made to make the program more simplistic was traversing through the entire wordlist. The wordlist is organized in alphabetic order, a better implementation would be to have the server interpret the first char (if its not a wild card) and go directly to the corresponding section. One suggestion of how to implement this in O(1) time would be a dictionary mapping each alphabet character to the sub-list of words in wordlist.txt that start with that character. However, you would still have to traverse through each sub-list. 

Project 2 Multi-threaded Server

Multithread_client.py
Thread-sever.py

The server has the same functionality except that it handles multiple clients simultaneously. The server uses the dispatcher function to continuously listen for new connections and assign a new connection socket for each client that sends a query. This connection is passed to a thread to execute the handle_client_function which receives & handles the query of the client and responds back to the client. This client has the feature of being able to send multiple queries and terminate on the command “quit”. I achieved the continuous prompt for queries by putting the socket.send() and socket.receive() of the client inside a while loop set to True. The input of the user is sent to the server, if the input is “quit” the program will break out of the while loop and then the socket communicating between client and socket will be closed.

A tradeoff I made was that I assumed the user inputs the correct format to the client. If you were to input a space or incorrect input the server raises an IndexError. A way to solve this is to edit the server, if the server receives an incorrect query it will return “no matches found”. Another tradeoff was that I wrote my own algorithm, if I were to do this assignment again, I would use other functions to check for matches, or a divide and conquer approach. Lastly, the send and receive buffer wasn’t enough to transmit the full amount of words; If the match was larger than 4096 bytes the program would only transit the first 4096 bytes. I solved this by sending an ending message by the server which prompted the user to stop receiving bytes from the server (This was done inside a while loop on the client side).

	
