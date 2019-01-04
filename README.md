# pyShells
Client and server model in python 3 using only standard library. 
Supports ssl encryption.

Run certs.sh to generate server cert and key

USAGE:

       git clone https://github.com/pyCity/pyShells

       cd pyShells; chmod +x certs.sh && ./certs.sh || echo Error running certs.sh

       python server.py 127.0.0.1 4444 --ssl

       python client.py 127.0.0.1 4444 --ssl


TODO: 
"get" and "put" functionality

https option

threading

persistence
