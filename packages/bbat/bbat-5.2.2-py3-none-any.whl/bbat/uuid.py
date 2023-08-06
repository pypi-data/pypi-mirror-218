

import uuid


def random_id(number=16):
    random_uuid = uuid.uuid4()
    random_id = random_uuid.hex[:number]
    return random_id