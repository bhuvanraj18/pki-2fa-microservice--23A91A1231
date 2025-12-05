# app/cron_generate.py

import datetime
from app.crypto_utils import load_decrypted_seed
from app.totp_utils import generate_totp

LOG_FILE = "/cron/last_code.txt"


def main():
    hex_seed = load_decrypted_seed()

    if not hex_seed:
        with open(LOG_FILE, "a") as f:
            f.write("No seed found\n")
        return

    code, _ = generate_totp(hex_seed)
    if not code:
        with open(LOG_FILE, "a") as f:
            f.write("Error generating TOTP\n")
        return

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")


if __name__ == "__main__":
    main()
