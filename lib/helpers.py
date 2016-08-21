# We're using Python's builtin random
# NOTE: This is not cryptographically strong
import random
import string

def read_hex(data):
    # Remove any spaces or newlines
    data = data.replace(" ", "").replace("\n", "")
    # Read the value as an integer from base 16 (hex)
    return int(data, 16)

def generate_random_string(alphabet=None, length=8, exact=False):
    if not alphabet:
        alphabet = string.ascii_letters + string.digits
    """
    The line below is called a list comprehension and is the same as:
    letters = []
    for i in range(length):
        # Select a random letter from the alphabet and add it to letters
        letters.append(random.choice(alphabet))
    # Join the letters together with no separator
    return ''.join(letters)
    """
    if not exact:
        length = random.randint(length-4 if length-4 > 0 else 1,length+4)
    return ''.join(random.choice(alphabet) for x in range(length))
