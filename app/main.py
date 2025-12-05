from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time

from app.crypto_utils import (
    load_private_key,
    decrypt_seed,
    generate_totp_code,
    verify_totp_code,
    SEED_FILE_PATH,
)

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_endpoint(body: SeedRequest):
    try:
        private_key = load_private_key()
        seed = decrypt_seed(body.encrypted_seed, private_key)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE_PATH, "w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE_PATH, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)
    remaining = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": remaining}

@app.post("/verify-2fa")
def verify_2fa(body: VerifyRequest):
    if not os.path.exists(SEED_FILE_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE_PATH, "r") as f:
        seed = f.read().strip()

    valid = verify_totp_code(seed, body.code)
    return {"valid": valid}

@app.get("/health")
def health():
    return {"status": "ok"}
