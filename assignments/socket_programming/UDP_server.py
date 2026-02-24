import socket
import sys
import time
import threading

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

def handle_client(sock, d, client_addr):
    connectionId = d.decode('utf-8').strip().split()[1]
    if connectionId in connections:
        reply = f"RESET {connectionId}"
    else:
        connections[connectionId] = time.time()
        reply = f"OK {connectionId} {client_addr[0]} {client_addr[1]}"

    sock.sendto(reply.encode('utf-8'), client_addr)

try:
    # create socket for all UDP communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.settimeout(1)
except socket.timeout:
    sys.exit()

connections = {}  # dictionary pairing: id -> timestamp
last_request_time = time.time()

while True:
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

    try:
        data, addr = sock.recvfrom(1024) # for small msgs (1KB dedicated): HELLO ID
        last_request_time = time.time()
        # threading improved parallel performance
        threading.Thread(
            target=handle_client,
            args=(sock, data, addr)
        ).start()

    except socket.timeout:
        pass
    except KeyboardInterrupt:
        break

sock.close()