# app/totp_utils.py

import base64
import time
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """Convert 64-character hex seed → Base32 encoding for TOTP."""
    raw_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(raw_bytes).decode("utf-8")


def generate_totp(hex_seed: str):
    """
    Generate current TOTP code and remaining validity (seconds).

    Returns:
        (code: str, remaining: int)
    """
    try:
        base32_seed = hex_to_base32(hex_seed)

        totp = pyotp.TOTP(
            base32_seed,
            digits=6,
            interval=30,
            digest="sha1",  # standard TOTP
        )

        code = totp.now()
        remaining = 30 - (int(time.time()) % 30)

        return code, remaining

    except Exception as e:
        print("TOTP generation error:", e)
        return None, None


def verify_totp(hex_seed: str, code: str) -> bool:
    """Verify TOTP with ±1 time window (±30 seconds)."""
    try:
        base32_seed = hex_to_base32(hex_seed)

        totp = pyotp.TOTP(
            base32_seed,
            digits=6,
            interval=30,
            digest="sha1",
        )

        return totp.verify(code, valid_window=1)

    except Exception as e:
        print("Verification error:", e)
        return False
