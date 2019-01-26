#!/usr/bin/env python3
import socket
import sys
import argparse
import ssl
import time

"""
Author       - pyCity
Date         - 1/22/2019
Version      - 2.0

Usage:       - python server.py --ssl 127.0.0.1 4444
             - Run setup.sh to generate certs

Description: - Handler for client.py Supports SSL encryption using
             - a DHE-RSA-AES256-SHA256 cipher.

"""

def get_args():
    """Define host, port, and encryption variables"""

    parser = argparse.ArgumentParser(description="Python tcp server")
    parser.add_argument("host", help="IP address to bind for listening")
    parser.add_argument("port", help="Port to bind for listening", type=int)
    parser.add_argument("--ssl", help="Enable SSL encryption", action="store_true")

    # Array of parsed arguments
    args = parser.parse_args()
    host, port, enc = args.host, args.port, args.ssl
    return host, port, enc



def wrap_sock(enc=False):
    """Create and wrap socket"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if enc == True:
            print("SSL encryption enabled")
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.set_ciphers('DHE-RSA-AES256-SHA256')
            context.load_dh_params("dhparam.pem")
            context.load_cert_chain("server.crt", "server.key")
            s = context.wrap_socket(s, do_handshake_on_connect=True, server_side=True)
        return s
    except socket.error as msg:
        print("Socket creation error: {}".format(str(msg)))
        s.close()
        sys.exit()



def bind_sock(s, host, port):
    """Bind socket to port and wait for client to connect. Avoid recursion with a while loop and time.sleep()."""

    max = 10
    attempts = 0
    while attempts < max:
        try:
            print("Binding port: " + str(port))
            s.bind((host, port))
            print("Listening for clients...")
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
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")

    except KeyboardInterrupt:
        conn.close()
        s.close()
        sys.exit()



if __name__ == "__main__":
    host, port, enc = get_args()
    s = bind_sock(wrap_sock(enc), host, port)
    handle(s)
