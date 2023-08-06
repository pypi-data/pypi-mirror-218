import binascii

def Decode(s: str) -> bytes:
    """
    Decode a Base16-encoded string to bytes.

    Args:
        s (str): The Base16-encoded string.

    Returns:
        bytes: The decoded bytes.
    """
    return binascii.unhexlify(s)

def Encode(b: bytes) -> str:
    """
    Encode bytes to a Base16-encoded string.

    Args:
        b (bytes): The bytes to encode.

    Returns:
        str: The Base16-encoded string.
    """
    return binascii.hexlify(b).decode('utf-8').upper()
