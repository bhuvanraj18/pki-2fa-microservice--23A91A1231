#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from app.crypto_utils import SEED_FILE_PATH, generate_totp_code

def main():
    if not os.path.exists(SEED_FILE_PATH):
        print("Seed not decrypted yet", flush=True)
        return

    with open(SEED_FILE_PATH, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}", flush=True)

if __name__ == "__main__":
    main()
