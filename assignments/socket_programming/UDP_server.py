import socket
import sys
import time
import threading

# get values from command prompt input
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

connections = {}  # dictionary pairing: id -> timestamp

# handle client connection, validate connection ID and generate response
def handle_client(sock, d, client_addr):
    connectionId = d.decode('utf-8').strip().split()[1]
    if connectionId in connections:     # ID in use
        reply = f"RESET {connectionId}"
    else:
        connections[connectionId] = time.time()
        reply = f"OK {connectionId} {client_addr[0]} {client_addr[1]}"
    # send response to client
    sock.sendto(reply.encode('utf-8'), client_addr)

# create socket for all UDP communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.settimeout(1)

last_request_time = time.time()

while True:
    # get current time
    now = time.time()

    # remove expired IDs (older than 60 seconds)
    living_connections = {}
    for connId, connTime in connections.items():
        if (now - connTime) < 60:
            living_connections[connId] = connTime
    connections = living_connections

    # server idle timeout (5 minutes)
    if (now - last_request_time) > 300:
        break

    # receive message from client and call handle_client()
    try:
        data, addr = sock.recvfrom(1024) # for small msgs (1KB dedicated): HELLO ID
        last_request_time = time.time()
        # threading for improved parallel performance
        threading.Thread(
            target=handle_client,
            args=(sock, data, addr)
        ).start()

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        break

sock.close()