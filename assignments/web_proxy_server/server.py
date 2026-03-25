from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
server_name = sys.argv[1]
server_port = int(sys.argv[2])
tcpSerSock.bind((server_name, server_port))
tcpSerSock.listen(1)
# Fill in end.
while 1:
    # Strat receiving data from the client
    print('\n\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()# Fill in start.
    if not message:
        tcpCliSock.close()
        continue # Fill in end.
    print("--Message--\n", message)
    # Extract the filename from the given message
    #print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    #print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    #print(filetouse)
    try:
        # Check wether the file exist in the cache
        cache_name = filename.replace("/", "_")
        f = open(cache_name, "rb")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
        tcpCliSock.send(b"Content-Type:text/html\r\n")
        # Fill in start.
        tcpCliSock.sendall(outputdata)
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            print("Cache miss")
            # Parse host + path
            parts = filename.split("/", 1)

            # Handle invalid requests (e.g., favicon.ico)
            if len(parts) == 1:
                tcpCliSock.send(b"HTTP/1.0 204 NO CONTENT\r\n\r\n")
                tcpCliSock.close()
                continue

            host = parts[0]
            path = "/" + parts[1]

            print("Host:", host)
            print("Path:", path)
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
            hostn = filename.replace("www.","",1)
            #print(hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((host, 80))
                request_line = (
                    f"GET {path} HTTP/1.0\r\n"
                    f"Host: {host}\r\n"
                    f"Connection: close\r\n\r\n"
                )
                c.sendall(request_line.encode())
                # Fill in end.
                # Create a temporary file on this socket and ask port 80
                #for the file requested by the client
                response = b""
                while True:
                    data = c.recv(4096)
                    if not data:
                        break
                    response += data
                #fileobj = c.makefile('r', 0)
                #fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                # Fill in start.
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                cache_name = filename.replace("/", "_")
                tmpFile = open(cache_name, "wb")
                # Fill in start.
                tmpFile.write(response)
                tmpFile.close()
                tcpCliSock.sendall(response)
                # Fill in end.
            except:
                print("Illegal request")
                tcpCliSock.send(b"HTTP/1.0 404 NOT FOUND\r\n\r\n")
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send(b"HTTP/1.0 404 NOT FOUND\r\n\r\n")
            # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end