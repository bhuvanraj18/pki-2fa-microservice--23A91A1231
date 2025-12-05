import sys
sys.path.append("/srv/app")

from datetime import datetime, timezone
from app.crypto_utils import SEED_FILE_PATH, generate_totp_code

def main():
    try:
        code, valid_for = generate_totp_code()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - 2FA Code: {code}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
