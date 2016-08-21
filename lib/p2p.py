import socket
import threading

from lib.comms import StealthConn
from lib.files import p2p_download_file

# Keep track of where our server is
# This is primarily so we don't try to talk to ourselves
server_port = 1337

def find_bot():
    print("Finding another bot...")
    port = 1337
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        if port == server_port:
            # Don't connect to yourself, silly bot!
            port += 1
        else:
            try:
                print("Found bot on port %d" % port)
                conn.connect(("localhost", port))
                sconn = StealthConn(conn, client=True)
                return sconn
            except socket.error:
                print("No bot was listening on port %d" % port)
                port += 1

def echo_server(sconn):
    while 1:
        data = sconn.recv()
        print("ECHOING>", data)
        sconn.send(data)
        if data == b'X' or data == b'exit':
            print("Closing connection...")
            sconn.close()
            return

def accept_connection(conn):
    try:
        sconn = StealthConn(conn, server=True)
        # The sender is either going to chat to us or send a file
        cmd = sconn.recv()
        if cmd == b'ECHO':
            echo_server(sconn)
        elif cmd == b'FILE':
            p2p_download_file(sconn)
    except socket.error:
        print("Connection closed unexpectedly")

def bot_server():
    global server_port
    # Every bot is both client & server, so needs to listen for
    # connections. This is to allow for peer to peer traffic.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Real worms use shifting ports but for simplicity, we won't.
    # We'll also assume you may run another bot on your computer
    # so if something else is using 1337, we'll keep going up.
    while True:
        try:
            s.bind(("localhost", server_port))
            print("Listening on port %d" % server_port)
            break
        except socket.error:
            # Someone is already using that port -- let's go up one
            print("Port %d not available" % server_port)
            server_port += 1
    s.listen(5)

    while 1:
        print("Waiting for connection...")
        conn, address = s.accept()
        print("Accepted a connection from %s..." % (address,))
        # Start a new thread per connection
        # We don't need to specify it's a daemon thread as daemon status is inherited
        threading.Thread(target=accept_connection, args=(conn,)).start()
