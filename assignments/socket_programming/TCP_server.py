import socket
import sys
import time
import threading

##setting up socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

sock.bind((SERVER_IP, SERVER_PORT))
sock.listen(5)
sock.settimeout(1)

connections = {} # dictionary pairing: id -> timestamp
conn_lock = threading.Lock()
last_request_time = time.time()

def handle_client(conn, addr):
    try: 
        conn.settimeout(60)

        data = conn.recv(4096)
        if not data:
            return

        parts = data.decode().strip().split()
        if len(parts) < 2:
            return

        connId = parts[1]

        with conn_lock:
            if connId in connections:
                reply = f"RESET {connId}"
            else:
                connections[connId] = time.time()
                reply = f"OK {connId} {addr[0]} {addr[1]}"

        conn.sendall(reply.encode())

    except socket.timeout:
        pass
    finally:
        conn.close()


while True:
    now = time.time()

    # Remove expired IDs
    new_connections = {}
    for connId, connTime in connections.items():
        if (now - connTime) < 60:
            new_connections[connId] = connTime
    connections = new_connections

    # Idle timeout
    if (now - last_request_time) > 300:
        break

    try:
        conn, addr = sock.accept()
    except socket.timeout:
        continue

    last_request_time = time.time()

    threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    ).start()

sock.close()
