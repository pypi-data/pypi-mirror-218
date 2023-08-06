import hashlib
from typing import Union

def Encode(s: Union[bytes, bytearray]) -> str:
    # Create a SHA256 object
    sha256 = hashlib.sha256()

    # Update the SHA256 object with the input bytes
    sha256.update(s)

    # Return the hexadecimal digest of the SHA256 object
    return sha256.hexdigest()

def EncodeFile(s: str) -> str:
    # Create a SHA256 object
    sha256 = hashlib.sha256()

    # Open the file in binary mode
    with open(s, "rb") as f:
        # Read and update the SHA256 object in chunks
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sha256.update(chunk)

    # Return the hexadecimal digest of the SHA256 object
    return sha256.hexdigest()
