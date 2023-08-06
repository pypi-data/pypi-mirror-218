import os
import struct
from Crypto.Cipher import AES

# A constant key size of 256 bits for AES-256
KeySize = 256

# A constant block size of 128 bits for AES
BlockSize = 128

# A constant initialization vector size of 16 bytes for AES
IVSize = 16

def Encrypt(data: bytes, key: bytes) -> bytes:
    # Check the input parameters for null values
    if data is None or len(data) == 0:
        raise ValueError("data cannot be null or empty")
    if key is None or len(key) == 0:
        raise ValueError("key cannot be null or empty")

    # Check the key size for AES-256
    if len(key) * 8 != KeySize:
        raise ValueError(f"Invalid key size. Expected {KeySize} bits, got {len(key) * 8} bits.")

    # Create a new instance of the AES class with the specified key and block size
    aes = AES.new(key, AES.MODE_CBC)

    # Generate a random initialization vector and assign it to the AES instance
    iv = os.urandom(IVSize)
    aes.iv = iv

    # Pad the data to match the block size using PKCS#7 padding scheme
    padding = BlockSize // 8 - (len(data) % (BlockSize // 8))
    data += bytes([padding] * padding)

    # Encrypt the data using the AES instance
    ciphertext = aes.encrypt(data)

    # Return the encrypted data with the initialization vector as a byte array
    return iv + ciphertext

def Decrypt(data: bytes, key: bytes) -> bytes:
    # Check the input parameters for null values
    if data is None or len(data) == 0:
        raise ValueError("data cannot be null or empty")
    if key is None or len(key) == 0:
        raise ValueError("key cannot be null or empty")

    # Check the key size for AES-256
    if len(key) * 8 != KeySize:
        raise ValueError(f"Invalid key size. Expected {KeySize} bits, got {len(key) * 8} bits.")

    # Create a new instance of the AES class with the specified key and block size
    aes = AES.new(key, AES.MODE_CBC)

    # Read the initialization vector from the data
    iv = data[:IVSize]

    # Assign the initialization vector to the AES instance
    aes.iv = iv

    # Decrypt the data using the AES instance
    plaintext = aes.decrypt(data[IVSize:])

    # Unpad the data using PKCS#7 padding scheme
    padding = plaintext[-1]
    plaintext = plaintext[:-padding]

    # Return the decrypted data as a byte array
    return plaintext
