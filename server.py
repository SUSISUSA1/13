from flask import Flask, request
import json, os

app = Flask(__name__)
KEYS_FILE = "keys.json"

def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f)

@app.route("/check")
def check():
    key = request.args.get("key", "")
    keys = load_keys()
    if key in keys and keys[key]["active"]:
        return "valid", 200
    return "invalid", 403

@app.route("/add")
def add():
    secret = request.args.get("secret", "")
    if secret != os.environ.get("ADMIN_SECRET", "changeme"):
        return "forbidden", 403
    key = request.args.get("key", "")
    if not key:
        return "no key", 400
    keys = load_keys()
    keys[key] = {"active": True}
    save_keys(keys)
    return "added", 200

@app.route("/revoke")
def revoke():
    secret = request.args.get("secret", "")
    if secret != os.environ.get("ADMIN_SECRET", "changeme"):
        return "forbidden", 403
    key = request.args.get("key", "")
    keys = load_keys()
    if key in keys:
        keys[key]["active"] = False
        save_keys(keys)
        return "revoked", 200
    return "not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
