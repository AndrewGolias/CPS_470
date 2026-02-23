import socket
import sys

MSG = sys.argv[1]
if MSG != "HELLO":
    validMsg = False
else:
    validMsg = True
SERVER_IP = sys.argv[2]
SERVER_PORT = int(sys.argv[3])
CONNECTION_ID = sys.argv[4]

tries = 0 # track user input for new connection ID attempts (max 3 tries)

while validMsg and tries <= 3:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(60)
        message = f"{MSG} {CONNECTION_ID}"
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        data, addr = sock.recvfrom(1024)
        reply = data.decode().split()

        if reply[0] == "OK":
            print(f"Connection established {reply[1]} {reply[2]} {reply[3]}")
            sock.close()
            sys.exit(0)
        else:
            print(f"Connection Error {reply[1]}")
            sock.close()
    except socket.timeout:
        print(f"Connection Timeout")
    except ConnectionResetError:
        break

    tries += 1
    if tries <= 3:
        print("Enter a new connection ID")
        CONNECTION_ID = input(">>")

print("Connection Failure")