import time
import binascii
import os
import pytest

def generate_random_objectid() -> str:
    timestamp = int(time.time())
    rest = binascii.b2a_hex(os.urandom(8)).decode("ascii")
    return f"{timestamp:x}{rest}"

@pytest.fixture
def random_objectid():
    return generate_random_objectid()