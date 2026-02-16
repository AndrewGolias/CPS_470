import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

sock.bind((SERVER_IP, SERVER_PORT))
sock.settimeout(1)

connections = {}  # dictionary pairing: id -> timestamp
last_request_time = time.time()

while True:
    now = time.time()
    # remove expired IDs (older than 60 seconds)
    new_connections = {}
    for connId, connTime in connections.items():
        if (now - connTime) < 60:
            new_connections[connId] = connTime
    connections = new_connections
    # server idle timeout (5 minutes)
    if (now - last_request_time) > 300:
        break

    try:
        data, addr = sock.recvfrom(4096)
    except socket.timeout:
        continue

    last_request_time = time.time()

    client_data = data.decode()

    connId = data.decode().strip().split()[1]
    if connId in connections:
        reply = f"RESET {connId}"
    else:
        connections[connId] = time.time()
        reply = f"OK {connId} {addr[0]} {addr[1]}"

    sock.sendto(reply.encode(), addr)

sock.close()
