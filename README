Welcome to SkyNet
=================

Part 1 Brief Review
(full details: check docs)
-------------------
+ Add code to dh/__init__.py
   1. What choice of parameters are you deciding on for DH?
   2. What's the proper way to calculate the private, public and shared keys?
+ Modify the way ciphers are used in lib/comms.py
   1. What's your choice of cypher? Why did you select it?
   2. Are your messages vulnerable to tampering, replay or frequency analysis?

Usage: Solo
===========
smerity@pegasus:~/usyd/elec5616_proj/framework$ python3.2 bot.py
Listening on port 1337
Waiting for connection...
Enter command: mine
Mined and found Bitcoin address: 3pWw3v08MJO7lDyzXXQ68e0i5enL
Enter command: harvest
Found user pass: ('Bob', 'pmiMFK')
Enter command: download hello.signed
The given file doesn't exist on pastebot.net
Enter command: download hello.signed
Stored the received file as hello.signed
Enter command: download hello.fbi
The file has not been signed by the botnet master
Enter command: list
Files stored by this bot: hello.signed
Valuables stored by this bot: ['Bitcoin: 3pWw3v08MJO7lDyzXXQ68e0i5enL', 'Username/Password: Bob pmiMFK']
Enter command: upload valuables.txt
Saved valuables to pastebot.net/valuables.txt for the botnet master
Enter command: exit

Usage: Peer to Peer (Upload)
(Note: Requires two bots at the same time)
============================
BOT #1
------
smerity@pegasus:~/usyd/elec5616_proj/framework$ python3.2 bot.py
Port 1337 not available
Listening on port 1338
Waiting for connection...
Enter command: download hello.signed
Stored the received file as hello.signed
Enter command: list
Files stored by this bot: hello.signed
Valuables stored by this bot: []
Enter command: p2p upload hello.signed
Finding another bot...
Found bot on port 1337
Sending hello.signed via P2P
------
BOT #2
------
smerity@pegasus:~/usyd/elec5616_proj/framework$ python3.2 bot.py
Listening on port 1337
Waiting for connection...
Enter command: list
Files stored by this bot:
Valuables stored by this bot: []
Accepted a connection from ('127.0.0.1', 36381)...
Waiting for connection...
Receiving hello.signed via P2P
Stored the received file as hello.signed
Enter command: list
Files stored by this bot: hello.signed
Valuables stored by this bot: []

Usage: Peer to Peer (Echo)
(Note: Requires two bots at the same time)
==========================
smerity@pegasus:~/usyd/elec5616_proj/framework$ python3.2 bot.py
Listening on port 1337
Waiting for connection...
Enter command: p2p echo
Finding another bot...
Found bot on port 1338
Shared hash: c2bd47c3ac55f104c052dca02eaa6c9de22e7637370584e5d2ba3c9c81bf2ab8
Original data: b'ECHO'
Encrypted data: b'!qpz'
Sending packet of length 4
Echo> Test
Original data: b'Test'
Encrypted data: b'0WKA'
Sending packet of length 4
Receiving packet of length 4
Encrypted data: b'0WKA'
Original data: b'Test'
Echo> exit
Original data: b'exit'
Encrypted data: b'\x01JQA'
Sending packet of length 4
Receiving packet of length 4
Encrypted data: b'\x01JQA'
Original data: b'exit'
Enter command: exit

Notice: 'Test' and 'exit' are sent and received as the same encrypted message.
This means it's vulnerable to frequency analysis. When 'a' is sent multiple times,
it ends up "looping" as we're using a simple repeated XOR cypher.
This is something that should be fixed.
