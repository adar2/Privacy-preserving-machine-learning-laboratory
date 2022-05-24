import base64
from uuid import UUID


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return uuid_obj == uuid_to_test


def bytes_to_string(bytes: bytes) -> str:
    return base64.encodebytes(bytes).decode()


def string_to_bytes(string: str) -> bytes:
    return base64.decodebytes(string.encode())