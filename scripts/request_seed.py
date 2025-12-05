import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23A91A1231"  # CHANGE THIS
GITHUB_REPO_URL = "https://github.com/bhuvanraj18/pki-2fa-microservice--23A91A1231.git"

def main():
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key
    }

    response = requests.post(API_URL, json=payload)
    data = response.json()

    print(data)

    if "encrypted_seed" in data:
        with open("encrypted_seed.txt", "w") as f:
            f.write(data["encrypted_seed"])
        print("Encrypted seed saved to encrypted_seed.txt")

if __name__ == "__main__":
    main()
