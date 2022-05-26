import base64
import pickle
from uuid import UUID, uuid4


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def generate_uuid():
    return str(uuid4())


def bytes_to_string(bytes: bytes) -> str:
    return base64.encodebytes(bytes).decode()


def string_to_bytes(string: str) -> bytes:
    return base64.decodebytes(string.encode())


def serialize(obj: object) -> str:
    obj_bytes = pickle.dumps(obj)
    return bytes_to_string(obj_bytes)


def deserialize(obj_string: str) -> object:
    str_bytes = string_to_bytes(obj_string)
    return pickle.loads(str_bytes)
