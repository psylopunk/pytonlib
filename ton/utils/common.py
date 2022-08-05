from hashlib import sha256 as hasher
from base64 import b64encode
import codecs

def sha256(x):
    if not isinstance(x, bytes):
        x = codecs.encode(x, 'utf-8')

    h = hasher()
    h.update(x)
    return h.digest()

def str_b64encode(s):
    return b64encode(s.encode('utf-8')).decode('utf-8') if s and isinstance(s, str) else None

def bytes_b64encode(s):
    return None if s is None else b64encode(s).decode('utf-8')