# pyShells
Client and server model in python 3 using only standard library. 

TIP: ncat --ssl listener works just as well as client.py

Run setup.sh to generate server cert and key

USAGE:

       git clone https://github.com/pyCity/pyShells

       cd pyShells; chmod +x setup.sh && ./setup.sh || echo Error running setup.sh

       python server.py 127.0.0.1 4444 --ssl

       python client.py 127.0.0.1 4444 --ssl


TODO: 
"get" and "put" functionality

https option

threading

persistence
