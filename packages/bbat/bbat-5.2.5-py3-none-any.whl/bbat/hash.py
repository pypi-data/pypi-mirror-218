
import hashlib
import uuid


def random_id(number=16):
    random_uuid = uuid.uuid4()
    random_id = random_uuid.hex[:number]
    return random_id


def md5(string, encoding=True):
    s = string.encode('utf8') if encoding else string
    return hashlib.md5(s).hexdigest()