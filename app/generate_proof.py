import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def get_latest_commit():
    """Return latest commit hash as a string."""
    commit = subprocess.check_output(
        ["git", "log", "-1", "--format=%H"]
    ).decode().strip()
    return commit


def load_private_key():
    """Load student's private key."""
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def sign_commit(commit_hash: str, private_key):
    """Sign commit hash using RSA-PSS SHA256."""
    signature = private_key.sign(
        commit_hash.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def encrypt_signature(signature: bytes):
    """Encrypt signature using instructor public key."""
    with open("instructor_public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    encrypted = public_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted


def main():
    commit_hash = get_latest_commit()
    print("Commit Hash:", commit_hash)

    private_key = load_private_key()
    signature = sign_commit(commit_hash, private_key)

    encrypted = encrypt_signature(signature)
    encoded = base64.b64encode(encrypted).decode()

    print("\nEncrypted Signature (Base64):")
    print(encoded)

    # Save to file for submission
    with open("encrypted_signature.b64", "w") as f:
        f.write(encoded)

    print("\nSaved to encrypted_signature.b64")


if __name__ == "__main__":
    main()
