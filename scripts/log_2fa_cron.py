#!/usr/bin/env python3
import sys, os
from datetime import datetime, timezone

# Make sure Python can see the app module
sys.path.append("/srv/app")
sys.path.append("/srv/app/app")

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
#!/usr/bin/env python3
import sys, os
from datetime import datetime, timezone

# Make sure Python can see the app module
sys.path.append("/srv/app")
sys.path.append("/srv/app/app")

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
