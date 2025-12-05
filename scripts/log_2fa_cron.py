#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

# Dynamically add project root (parent of scripts/) to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # /app/scripts
PROJECT_ROOT = os.path.dirname(BASE_DIR)                   # /app
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.crypto_utils import SEED_FILE_PATH, generate_totp_code

def main():
    if not os.path.exists(SEED_FILE_PATH):
        print("Seed file missing")
        return

    code = generate_totp_code()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
