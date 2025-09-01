from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

DATA_FILE = "counter.json"
WEBHOOK_URL = "https://discord.com/api/webhooks/1412108717746290729/Zy_YI7HIMXAeIKGOQ0ew4teYVrGbcib8N-h4M-TwDNRkKyyR_FO3ah0tA09VLaafqYRU"  


if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"executionCount": 0, "messageId": None}


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


@app.route("/execute", methods=["POST"])
def execute():
    body = request.json
    username = body.get("username")
    display_name = body.get("displayName")

    if not username or not display_name:
        return jsonify({"success": False, "error": "Missing username or displayName"}), 400

    data["executionCount"] += 1

   
    embed = {
        "username": "SCP || EXECUTION",
        "embeds": [
            {
                "title": "Name - [ SCP || EXECUTION ] [ CREDIT - HENNE ]",
                "color": 0x9933FF,
                "fields": [
                    {"name": "⚡ EXECUTION", "value": str(data["executionCount"]), "inline": False},
                    {"name": "🎮 PLAYER", "value": f"**Username:** {username}\n**Display Name:** {display_name}", "inline": False}
                ],
            }
        ],
    }

    try:
        if data["messageId"]:
            url = WEBHOOK_URL + f"/messages/{data['messageId']}"
            requests.patch(url, json=embed)
        else:
            resp = requests.post(WEBHOOK_URL, json=embed)
            if resp.ok:
                data["messageId"] = resp.json().get("id")

        save_data()
        return jsonify({"success": True, "executionCount": data["executionCount"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/counter")
def counter():
    return jsonify({"executionCount": data["executionCount"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
