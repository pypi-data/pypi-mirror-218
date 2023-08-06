import hashlib
import os
import secrets
import base64

def hash_password(password):
    salt = os.urandom(16)
    pepper = b'$velo@hash?'
    combined = salt + password.encode() + pepper

    for _ in range(20):
        combined = hashlib.sha3_512(combined).digest()
        combined = hashlib.sha3_256(combined).digest()

    iterations = 2000000
    for _ in range(iterations):
        combined = hashlib.sha3_512(combined).digest()

    final_hash = '$velo@hash?' + salt.hex() + combined.hex()
    return final_hash

def verify_password(password, hashed_password):
    prefix = '$velo@hash?'
    salt_hex = hashed_password[len(prefix): len(prefix) + 32]
    combined_hash = hashed_password[len(prefix) + 32:]
    combined = bytes.fromhex(salt_hex) + password.encode() + prefix.encode()

    for _ in range(20):
        combined = hashlib.sha3_512(combined).digest()
        combined = hashlib.sha3_256(combined).digest()

    iterations = 2000000
    for _ in range(iterations):
        combined = hashlib.sha3_512(combined).digest()

    combined_hex = combined.hex()
    generated_hash = prefix + salt_hex + combined_hex
    return generated_hash == hashed_password


def change_password(old_password, new_password, hashed_password):
    is_valid = verify_password(old_password, hashed_password)
    if is_valid:
        new_hashed_password = hash_password(new_password)
        return new_hashed_password
    else:
        raise ValueError("Invalid old password. Password change failed.")

def generate_salt():
    salt = os.urandom(32)
    salt_base64 = base64.urlsafe_b64encode(salt)
    return salt_base64

def generate_pepper():
    pepper = secrets.token_bytes(64)
    return pepper

def encrypt_data(data, key):
    encoded_data = data.encode()
    cipher_text = b""
    for i in range(len(encoded_data)):
        key_c = key[i % len(key)]
        encoded_char = (encoded_data[i] + key_c) % 256
        cipher_text += bytes([encoded_char])
    encrypted_data = base64.urlsafe_b64encode(cipher_text).decode()
    return encrypted_data

def decrypt_data(encrypted_data, key):
    decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
    plain_text = ""
    for i in range(len(decoded_data)):
        key_c = key[i % len(key)]
        decoded_char = (decoded_data[i] - key_c) % 256
        plain_text += chr(decoded_char)
    return plain_text

def generate_key():
    key = secrets.token_bytes(32)
    return key

def RouterID1(node=None, clock_seq=None):
    from time import time
    import random

    nanoseconds = int(time() * 1e9)
    timestamp = int(nanoseconds / 100) + 0x01b21dd213814000
    clock_seq = clock_seq if clock_seq is not None else random.getrandbits(14)

    timestamp_bytes = timestamp.to_bytes(8, 'big')
    clock_seq_bytes = clock_seq.to_bytes(2, 'big')
    node = node.to_bytes(10, 'big') if node is not None else os.urandom(10)

    return b"".join([timestamp_bytes[:6], timestamp_bytes[6:], clock_seq_bytes, node])

def RouterID4():
    return os.urandom(16)

def RouterID3(namespace, name):
    namespace_bytes = namespace if isinstance(namespace, bytes) else namespace.encode()
    name_bytes = name.encode() if isinstance(name, str) else name

    hash_value = hashlib.md5(namespace_bytes + name_bytes).digest()
    hash_value = hash_value[:16] 

    return bytes(hash_value)

def RouterID5(namespace, name):
    namespace_bytes = namespace if isinstance(namespace, bytes) else namespace.encode()
    name_bytes = name.encode() if isinstance(name, str) else name

    hash_value = hashlib.sha1(namespace_bytes + name_bytes).digest()
    hash_value = hash_value[:16]

    return bytes(hash_value)