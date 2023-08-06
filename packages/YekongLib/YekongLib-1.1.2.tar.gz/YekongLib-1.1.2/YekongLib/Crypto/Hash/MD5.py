import hashlib
from typing import Union

def Encode(s: Union[bytes, bytearray]) -> str:
    # Create an MD5 object
    md5 = hashlib.md5()

    # Update the MD5 object with the input bytes
    md5.update(s)

    # Return the hexadecimal digest of the MD5 object
    return md5.hexdigest()

def EncodeFile(s: str) -> str:
    # Create an MD5 object
    md5 = hashlib.md5()

    # Open the file in binary mode
    with open(s, "rb") as f:
        # Read and update the MD5 object in chunks
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            md5.update(chunk)

    # Return the hexadecimal digest of the MD5 object
    return md5.hexdigest()
