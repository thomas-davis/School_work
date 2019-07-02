Assignment from CSE 3100. Not all of it is my work, since the assignment came with skeleton code, including the print_server() and close_server and create_server functions 

The goal is to develop a very generalized server. In this case, generalized means that it can do pretty
much anything! It is essentially a remote shell, but it is designed in a way that can be easily adapted
to more specific applications. You will write a server that receives incoming clients. Upon receiving a 
connecting client, the server creates a thread to handle that client. All clients are kept track of with 
a linked list starting from the global head variable. Take a look at some of the structures if you have
any questions about this. The client, once connected, can execute commands from the server. On the client
side, all the user has to do to run a command is add the 'execute' prefix to any command they want to run.
As an example, say the client wanted to run 'ls' on the server. After connecting, they would send

execute ls

to the server Another more interesting example would be sending 

execute python3 hello_python.py

to the server. The server will then execute this command and allow the client socket and executed program
to communicate back and forth. 

