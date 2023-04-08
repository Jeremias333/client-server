try:
    import sys
    import os
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '../'
            )
        )
    )
except:
    raise

import hashlib

def encrypt_message(message: str() or [str()] = "", passkey: str() = "3301"):
    # Generate a key from the hash value
    key = hashlib.sha256(passkey.encode()).digest()

    # Convert the text to bytes
    text_bytes = message.encode()

    # Encrypt the text with the key and convert to hexadecimal
    encrypted_text_bytes = bytearray()
    for i in range(0, len(text_bytes), len(key)):
        block = text_bytes[i:i+len(key)]
        if len(block) < len(key):
            block += b'\0' * (len(key) - len(block))
        encrypted_text_bytes += bytes([a ^ b for a, b in zip(block, key)])
    encrypted_text_hex = encrypted_text_bytes.hex()

    return encrypted_text_hex

def decrypt_message(message: str() or [str()] = "", passkey: str() = "3301"):
     # Generate a key from the hash value
    key = hashlib.sha256(passkey.encode()).digest()

    # Decrypt the text to bytes from the hexadecimal
    encrypted_text_bytes = bytes.fromhex(message)
    decrypted_text_bytes = bytearray()
    for i in range(0, len(encrypted_text_bytes), len(key)):
        block = encrypted_text_bytes[i:i+len(key)]
        decrypted_text_bytes += bytes([a ^ b for a, b in zip(block, key)])
    decrypted_text = decrypted_text_bytes.rstrip(b'\0').decode()

    return decrypted_text
