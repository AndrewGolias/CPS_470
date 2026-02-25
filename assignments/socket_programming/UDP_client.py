import socket
import sys

# get values from command prompt input
MSG = sys.argv[1]
SERVER_IP = sys.argv[2]
SERVER_PORT = int(sys.argv[3])
CONNECTION_ID = sys.argv[4]

# validate HELLO and connection ID length
if MSG != "HELLO" or len(CONNECTION_ID) != 4:
    sys.exit(1)

tries = 0 # track user input for new connection ID attempts (max 3 tries)

while tries <= 3: # allows for 3 inputs after initial failed attempt
    try:
        # create new socket for connection attempt
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)

        # build message to send to server
        message = f"{MSG} {CONNECTION_ID}"
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        data, addr = sock.recvfrom(1024)
        reply = data.decode().split()

        # check response from server
        if reply[0] == "OK":    # successful connection; end program
            print(f"Connection established {reply[1]} {reply[2]} {reply[3]}")
            sock.close()
            sys.exit(0)
        elif reply[0] == "RESET":   # successful connection; connection ID already in use
            print(f"Connection Error {reply[1]}")
            sock.close()
        else:   # unsuccessful connection
            raise socket.timeout
    except socket.timeout:
        print(f"Connection Timeout")
        sock.close()
    except Exception:
        sock.close()
        break

    tries += 1
    if tries <= 3:  # reattempt entering ID; give additional attempts if length is not 4
        print("Enter a new connection ID")
        CONNECTION_ID = input(">>")
        while len(CONNECTION_ID) != 4:
            CONNECTION_ID = input(">>")

print("Connection Failure")