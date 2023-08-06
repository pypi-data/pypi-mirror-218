import hashlib
from typing import Union

def Encode(s: Union[bytes, bytearray]) -> str:
    # Create a SHA512 object
    sha512 = hashlib.sha512()

    # Update the SHA512 object with the input bytes
    sha512.update(s)

    # Return the hexadecimal digest of the SHA512 object
    return sha512.hexdigest()

def EncodeFile(s: str) -> str:
    # Create a SHA512 object
    sha512 = hashlib.sha512()

    # Open the file in binary mode
    with open(s, "rb") as f:
        # Read and update the SHA512 object in chunks
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sha512.update(chunk)

    # Return the hexadecimal digest of the SHA512 object
    return sha512.hexdigest()
