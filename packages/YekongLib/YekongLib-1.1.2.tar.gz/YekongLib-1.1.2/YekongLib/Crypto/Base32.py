import base64

def Decode(s: str) -> bytes:
    """
    Decode a Base32-encoded string to bytes.

    Args:
        s (str): The Base32-encoded string.

    Returns:
        bytes: The decoded bytes.
    """
    return base64.b32decode(s)

def Encode(b: bytes) -> str:
    """
    Encode bytes to a Base32-encoded string.

    Args:
        b (bytes): The bytes to encode.

    Returns:
        str: The Base32-encoded string.
    """
    return base64.b32encode(b).decode('utf-8')
