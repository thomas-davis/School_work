#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <dirent.h>
#include <time.h>
#include <signal.h>

#define CLIENT_QUEUE_LEN 10
#define SERVER_PORT 10101
#define SERVER_TIMEOUT 5
#define CLIENT_TIMEOUT 5
#define COMMAND_MAX_SIZE 256

// The structure that holds all the data the client needs
typedef struct ClientData {
	struct sockaddr_in *client;
	int socket_id;
	char continue_client;
	pthread_t thread_id;
} ClientData;

// The structure that composes the list of client data
typedef struct ClientSlot {
	ClientData *data;
	struct ClientSlot *prev;
	struct ClientSlot *next;
} ClientSlot;

pthread_mutex_t mutex;

int server_id = -1;
ClientSlot *head;


int create_server(int port);
ClientData *create_client(int client_id, struct sockaddr_in *client);
void start_client_thread(ClientData *config);
void *handle_client(void *targs);
int kill_client(ClientSlot *slot);
int reap_clients();
char **space_parse(char *str, int *count);

// Handles any error in the sockets:
void check_error(int status) {
    if (status < 0) {
        printf("Socket error: [%s]\n", strerror(errno));
    }
}

// Creates a server and returns its socket id.
int create_server(int port) {
    int sid = socket(PF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    int status = bind(sid, (struct sockaddr*)&addr, sizeof(addr));
    check_error(status);

    status = listen(sid, CLIENT_QUEUE_LEN);
    check_error(status);

    return sid;
}

// Processed by the SIGINT signal.
void close_server() {
	// Closing all the client connections:
	ClientSlot *cur = head;
	while (cur) {
		ClientSlot *prev = cur;
		cur = cur->next;
		kill_client(prev);
	}
	
	// Closing the server:
	close(server_id);

	fprintf(stderr, "Server exited normally.\n");
	exit(0);
}

void print_clients() {
	ClientSlot *cur = head;
	fprintf(stderr, "Clients List: ");
	while (cur) {
		fprintf(stderr, "%ud, ", cur->data->socket_id);
		cur = cur->next;
	}
	fprintf(stderr, "\n");
}

// ----------------------------------- ONLY ADD CODE BELOW THIS! ----------------------------------- //

// The main function:
int main(int argc, char *argv[]) {

	head = NULL;
	fd_set fd_select;
	struct timeval timeout;
	int port = SERVER_PORT;

	if (argc > 1)
		port = atoi(argv[1]);
	
	// Setting up the server to allow port reuse, and for accepts to be non-blocking.	
	server_id = create_server(port);
	if (setsockopt(server_id, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int)) < 0)
		printf("setsockopt(SO_REUSEADDR) failed\n");
	printf("Created server on port %d\n", port);

	char continue_server = 1;
	pthread_mutex_init(&mutex, NULL);

	signal(SIGINT, close_server);
        //run on ctrl+C

	// While loop for accepting clients into the server:
	while (continue_server) {
	
		FD_ZERO(&fd_select); /* clear the set */
		FD_SET(server_id, &fd_select); /* add our file descriptor to the set */

		// Waiting for the server to have an incoming client:
		timeout.tv_sec = SERVER_TIMEOUT;
		timeout.tv_usec = 0;
		int sel_option = select(server_id + 1, &fd_select, NULL, NULL, &timeout);

		// Only accepting a client if the server is still supposed to be running:
		if (continue_server) {
			reap_clients();
			if (FD_ISSET(server_id, &fd_select)) {
				fprintf(stderr, "Accepting client...\n");
                                struct sockaddr_in client_addr; 
                                int client_addr_size= sizeof(client_addr); 

                                int client_id= accept(server_id, &client_addr, &client_addr_size);  
			        ClientData* client= create_client(client_id, &client_addr);  	
                                start_client_thread(client); 
                                print_clients();
				/*
				 * If we get inside of this if statement, then there is a client ready to be accepted. 
				 * Call accept, then create the client thread to handle it
				 * 
				 */

			}	
		}

		// If a select error occurs, then we close.
		if (sel_option < 0) {
			fprintf(stderr, "\nSelect error, closing...");
			break;
		}

	}

	close_server();
	return 0;
}

/*
 * TODO: Implement this function.
 * 
 * This function starts the client thread based on the give client data
 */
void start_client_thread(ClientData *config) {
        pthread_t thread_id; 
        config->thread_id=thread_id; 
	pthread_create(&config->thread_id, NULL, handle_client, (void*) config);  
}

/*
 * TODO: Complete this function
 * 
 * Creates the client by defining its ClientData structure, filling it, and adding it to the global list.
 * Returns a pointer to the ClientData structure created.
 */
ClientData *create_client(int client_id, struct sockaddr_in *client) {
        //always adding to end of LL. Not sure it matters.
        struct ClientData* newclient= malloc(sizeof(struct ClientData)); 
        newclient->continue_client=1; 
        newclient->client=client; 
        newclient->socket_id=client_id;         
        struct ClientSlot* newnode= malloc(sizeof(struct ClientSlot)); ;
        newnode->next=NULL; 
        newnode->prev=NULL; 
        newnode->data=newclient; 
        ClientSlot* cur= head; 
        //lock while we modify LL
        //critical section: 
        pthread_mutex_lock(&mutex); 
        if(cur==NULL)
             head=newnode; 
        else{
             while(cur->next != NULL)
                 cur=cur->next; 
             //cur now points to last nonnull node; 
             cur->next=newnode; 
             newnode->prev=cur; 
        }  
        //critical section ends
        pthread_mutex_unlock(&mutex); 
        return newclient; 
}

/*
 * Finds clients that have been closed by the client and deallocates them. Feel free to use any of the 
 * functions you have already written in here (hint hint). Also make sure to remove the client from the
 * list of clients.
 * Return the number of clients reaped.
 */
int reap_clients() {
        int killcount=0;
        ClientSlot* temp;
        pthread_mutex_lock(&mutex); 
        //delete from start of doubly linked list (so we modify head): 
        while(head != NULL && head->data->continue_client==0){ 
            temp=head; 
            head=head->next; 
            kill_client(temp); 
            killcount++; 
        }
        ClientSlot* cur=head;  
        //now either cur is null, or it is a node which shouldn't be deleted
        //delete from middle/end of DLL:
        while(cur != NULL){ 
            while(cur != NULL && cur->data->continue_client==1) 
                cur=cur->next; 
            //at this point either cur is null (and we're done), or we have to delete cur 
            if(cur==NULL){
                pthread_mutex_unlock(&mutex); 
                return killcount; 
             }else{
                temp=cur->next;
                cur->prev->next=temp; 
                temp->prev=cur->prev; 
                kill_client(cur); 
                killcount++;
                cur=temp; 
            }
        }
        pthread_mutex_unlock(&mutex); 
        return killcount;
}

// Kills the client from an exterior source and allows it to exit normally.
     /*
     * 
     * Must wait for client thread to finish
     * Must free any memory and close any file descriptors associated with the given client thread.
     * 
     * Returns 1 on success and 0 on failure.
     */
int kill_client(ClientSlot *slot) {
	// Telling the client thread to exit.
	slot->data->continue_client = 0;
        if(pthread_join(slot->data->thread_id, NULL) ||  close(slot->data->socket_id)==-1) 
            return 0;  
        free(slot->data);
	return 1;
}

// Handles an incoming client connection.
void *handle_client(void *targs) {
	ClientData *args = (ClientData*) targs;
        
        //char* welcomestring ="welcome to my cool fun server\ntype \"execute [COMMAND]\" to run:\n";
        ///dprintf(args->socket_id, welcomestring);     	
	// Declaring select utilites:
	fd_set read_fds;
	struct timeval timeout;

        pid_t pid; 
	while(args->continue_client) {

		timeout.tv_sec = CLIENT_TIMEOUT;
		timeout.tv_usec = 0;
		FD_ZERO(&read_fds); /* clear the set */
		FD_SET(args->socket_id, &read_fds); /* add our file descriptor to the set */
		int sel_result = select(args->socket_id + 1, &read_fds, NULL, NULL, &timeout);

		if (args->continue_client && sel_result > 0) {
			char buf[COMMAND_MAX_SIZE + 1];
			int bytes = read(args->socket_id, buf, COMMAND_MAX_SIZE);
			
			if (bytes == 0){
				break;
                        }
			buf[bytes] = 0;
			int arg_count;
			char **command = space_parse(buf, &arg_count);
                        if(bytes!=0 && arg_count==0)
                             break;
                             //they only entered white space or a new line
			if (!strcmp(command[0], "execute")) {
				printf("Executing command %s on client %u\n", command[0], args->socket_id); 
                                pid_t pid = fork();
                                if(pid==0){ 
                                    dup2(args->socket_id, 0);  
                                    dup2(args->socket_id, 1);  
                                    if(execvp(command[1], command+1)==-1)
                                        fprintf(stderr, "failed to execute command: %s", command[1]); 
                               } 
				/*
                 * TODO:
                 * The client wants the server to execute a command.
                 * 
                 * You must fork a child process and forward all input and output from the child process
                 * to the client's socket. (Hint: This is a lot simpler than it sounds!)
                 * 
                 * The command to execute is given as the values in the command char** array. 
                 * Example: 
                 *  client> execute ls -al
                 *  server> 'prints output of $ ls -al'
                 */

			} else {
				printf("Invalid command: [%s]\n", command[0]);
			}
			    for (int i = 0; i < arg_count; i++)
			         free(*(command + i));
			    free(command);
		}

		if (sel_result < 0) {
			break;
		}
	}

	/*
	 * TODO: You have to add something here...
	 */

        //I'm not sure what to add, sorry I don't know what I'm missing. 

	args->continue_client = 0;
        int status; 

	return NULL;
}

/*
 * Function to get an array of strings that are parsed from the given string.
 * 
 * The returned array are all the space separated strings that are in the str parameter string.
 * Returned array should be allocated on the heap. Try to use as little memory as possible.
 * 
 * @param str - a null terminated character array.
 * @param count - a pointer to an integer that will be filled with the number of strings in the
 *      returned array of strings.
 * @returns an array of null terminated character arrays (array of strings). Allocated on the heap.
 */
char **space_parse(char *str, int *count){
    //TODO refactor. use two pointers for this, and get rid of the copy. I am a bad lazy programmer, so I'm leaving it in. 
    char copy[strlen(str)];   
    char* white_space_delims= " \n\t\v\f";
    //can use any white space delims
    *count=0; 
    //recent count
    strcpy(copy, str); 
    char** answer= malloc(COMMAND_MAX_SIZE*sizeof(char*)); 
    //We malloc a large chunk at first, then realloc at the end
    char* token=strtok(copy, white_space_delims); 
    while(token != NULL){
          char* buf= malloc(sizeof(token)); 
          //only allocate as much as we need
          strcpy(buf, token);
          answer[*count]=buf; 
          (*count)++; 
          token=strtok(NULL, white_space_delims);
    }
    answer[*count+1]=NULL; 
    //adding null onto the end
    answer= realloc(answer, (*count+1)*sizeof(char*));  
    return answer;     
}
