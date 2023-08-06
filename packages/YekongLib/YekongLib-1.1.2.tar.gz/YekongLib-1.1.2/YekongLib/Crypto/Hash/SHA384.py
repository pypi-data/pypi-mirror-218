import hashlib
from typing import Union

def Encode(s: Union[bytes, bytearray]) -> str:
    # Create a SHA384 object
    sha384 = hashlib.sha384()

    # Update the SHA384 object with the input bytes
    sha384.update(s)

    # Return the hexadecimal digest of the SHA384 object
    return sha384.hexdigest()

def EncodeFile(s: str) -> str:
    # Create a SHA384 object
    sha384 = hashlib.sha384()

    # Open the file in binary mode
    with open(s, "rb") as f:
        # Read and update the SHA384 object in chunks
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sha384.update(chunk)

    # Return the hexadecimal digest of the SHA384 object
    return sha384.hexdigest()
