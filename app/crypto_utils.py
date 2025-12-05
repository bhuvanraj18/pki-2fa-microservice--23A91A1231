import base64
import os
import pyotp
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SEED_FILE_PATH = "/data/seed.txt"

def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_seed(encrypted_seed_b64, private_key):
    ciphertext = base64.b64decode(encrypted_seed_b64)

    seed_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    seed = seed_bytes.decode().strip()

    if len(seed) != 64:
        raise ValueError("Invalid seed length")
    return seed

def hex_to_base32(hex_seed):
    raw = bytes.fromhex(hex_seed)
    return base64.b32encode(raw).decode()

def generate_totp_code(hex_seed):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.now()

def verify_totp_code(hex_seed, code):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.verify(code, valid_window=1)
