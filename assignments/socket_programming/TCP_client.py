import socket
import sys

MSG = sys.argv[1]
SERVER_IP = sys.argv[2]
SERVER_PORT = int(sys.argv[3])
CONNECTION_ID = sys.argv[4]

tries = 0 # track user input for new connection ID attempts (max 3 tries before failing)

while tries <= 3:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(60)
    try:
        message = f"{MSG} {CONNECTION_ID}"

        sock.connect((SERVER_IP, SERVER_PORT))
        sock.sendall(message.encode())
        data = sock.recv(4096)

        if not data:
            print("Connection Failure")
            break

        reply = data.decode().split()

        if reply[0] == "OK":
            print(f"Connection established {reply[1]} {reply[2]} {reply[3]}")
            sock.close()
            sys.exit(0)
        else:
            print(f"Connection Error {CONNECTION_ID}")
    except socket.timeout:
        print(f"Connection Timeout")
    except ConnectionResetError:
        break
    finally:
        sock.close()

    tries += 1

    if tries <= 3:
        print("Enter a new connection ID")
        CONNECTION_ID = input(">>")

print("Connection Failure")
