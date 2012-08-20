from hashlib import sha256
from Crypto.Random import get_random_bytes

def hash(string):
    return sha256(string).hexdigest()


random_bytes = get_random_bytes
