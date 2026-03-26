from socket import *
import sys

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server'
    )
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
server_name = sys.argv[1]
server_port = int(sys.argv[2])
tcpSerSock.bind((server_name, server_port))
tcpSerSock.listen(1)
try:
    while 1:
        # Start receiving data from the client
        print("\n\nReady to serve...")
        tcpCliSock, addr = tcpSerSock.accept()
        print("Received a connection from:", addr)
        message = tcpCliSock.recv(4096).decode()
        if not message:
            tcpCliSock.close()
            continue
        print("--Message--\n", message)
        # Extract the filename from the given message
        filename = message.split()[1].partition("/")[2]
        fileExist = "false"
        filetouse = "/" + filename
        try:
            # Check wether the file exist in the cache
            cache_name = filename.replace("/", "_")
            f = open(cache_name, "rb")
            outputdata = f.read()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            tcpCliSock.sendall(outputdata)
            print("Read from cache")
        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                print("Cache miss")
                # Parse host + path
                parts = filename.split("/", 1)

                # Handle invalid requests
                if len(parts) == 1:
                    tcpCliSock.send(b"HTTP/1.0 204 NO CONTENT\r\n\r\n")
                    tcpCliSock.close()
                    continue

                host = parts[0]
                path = "/" + parts[1]

                print("Host:", host)
                print("Path:", path)
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                try:
                    # Connect to the socket to port 80
                    c.connect((host, 80))
                    request_line = (
                        f"GET {path} HTTP/1.0\r\n"
                        f"Host: {host}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    c.sendall(request_line.encode())
                    # Read the response into buffer
                    response = b""
                    while True:
                        data = c.recv(4096)
                        if not data:
                            break
                        response += data
                    # Create a temporary file on this socket and ask port 80
                    cache_name = filename.replace("/", "_")
                    # Create a new file in the cache for the requested file.
                    tmpFile = open(cache_name, "wb")
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile.write(response)
                    tmpFile.close()
                    tcpCliSock.sendall(response)
                except:
                    print("Illegal request")
                    tcpCliSock.send(b"HTTP/1.0 404 NOT FOUND\r\n\r\n")
            else:
                # HTTP response message for file not found
                tcpCliSock.send(b"HTTP/1.0 404 NOT FOUND\r\n\r\n")

        # Close the client socket
        tcpCliSock.close()
        # CLose the server socket
    tcpSerSock.close()
except KeyboardInterrupt:
    print("Closing program")
    tcpCliSock.close()
    tcpSerSock.close()
    sys.exit()
