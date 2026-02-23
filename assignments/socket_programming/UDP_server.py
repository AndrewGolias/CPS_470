import socket
import sys
import time

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.settimeout(60)
except socket.timeout:
    sys.exit()

connections = {}  # dictionary pairing: id -> timestamp
last_request_time = time.time()

while True:
    now = time.time()
    # remove expired IDs (older than 60 seconds)
    living_connections = {}
    for connId, connTime in connections.items():
        if (now - connTime) < sock.gettimeout():
            living_connections[connId] = connTime
    connections = living_connections
    # server idle timeout (5 minutes)
    if (now - last_request_time) > 300:
        break

    try:
        data, addr = sock.recvfrom(1024) # for small msgs (1KB dedicated): HELLO ID
        last_request_time = time.time()

        client_data = data.decode()

        connId = data.decode().strip().split()[1]
        if connId in connections:
            reply = f"RESET {connId}"
        else:
            connections[connId] = time.time()
            reply = f"OK {connId} {addr[0]} {addr[1]}"

        sock.sendto(reply.encode(), addr)
    except socket.timeout or KeyboardInterrupt:
        break

sock.close()
