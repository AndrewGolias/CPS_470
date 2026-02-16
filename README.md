# CPS_470

### Socket Programming: /assignments/socket_programming
Simple client & server programs able to communicate with each other using sockets, according to the following protocol:

Testing:
    ConnectionID = 2876
    Server_IP = 127.0.0.1
    Server_Port = 34567
    
+ Client (initiator): sends msg to server with string followed by a space and a string containing a random 4-digit number - the connection ID
+ e.g. HELLO 2876

``` python UDP_client.py HELLO 127.0.0.1 34567 2876 ```


+ Server (listener): opens a port on a specified number and waits for a client to connect at the listening port. Receives the client's msg through a UDP datagram socket or TCP segment socket

``` python UDP_server.py 127.0.0.1 34567  ```

Server reads client's msg and responds:
+ OK - e.g. OK 9876 192.168.0.10 12345
+ Error - e.g. RESET 9876
+ Timeout (server or ConnectionID)

