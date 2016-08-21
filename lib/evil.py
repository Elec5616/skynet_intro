# We're using Python's builtin random
# NOTE: This is not cryptographically strong
import random
import time

from lib.helpers import generate_random_string

def bitcoin_mine():
    frames = "\\|/-"
    for i in range(8):
        print("\r%c" % frames[i % len(frames)], end="")
        time.sleep(0.1)
    print()
    # Bitcoin addresses start with a 3 or 1
    return random.choice("13") + generate_random_string(length=30)

def harvest_user_pass():
    names = "Bob Tim Ben Adam Lois Julie Daniel Lucy Sam Stephen Matt Luke Jenny Becca".split()
    return random.choice(names), generate_random_string(length=10)
