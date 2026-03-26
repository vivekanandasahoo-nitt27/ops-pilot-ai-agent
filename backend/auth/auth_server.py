from flask import Flask, redirect, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ GLOBAL TOKEN STORAGE
USER_TOKEN = None

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:5000/callback"


# 🔐 Login Route
@app.route("/login")
def login():
    return redirect(
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid profile email"
    )


# 🔁 Callback Route
@app.route("/callback")
def callback():
    global USER_TOKEN

    code = request.args.get("code")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(token_url, json=payload)
    tokens = response.json()

    USER_TOKEN = tokens.get("access_token")

    print("✅ TOKEN STORED:", USER_TOKEN[:10] if USER_TOKEN else "None")

    return "✅ Login successful! Return to OpsPilot UI."


# 🔓 Get Token
@app.route("/get-token")
def get_token():
    global USER_TOKEN
    return {"token": USER_TOKEN}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)