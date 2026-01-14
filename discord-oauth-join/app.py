from flask import Flask, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
GUILD_ID = os.environ["GUILD_ID"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_res = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()

    access_token = token_res["access_token"]

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    requests.put(
        f"https://discord.com/api/guilds/{GUILD_ID}/members/{user['id']}",
        headers={
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"access_token": access_token}
    )

    return "✅ You have joined the server! You may close this tab."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
