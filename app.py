from flask import Flask, request, jsonify
import os

app = Flask(__name__)
API_KEY = os.getenv("OSS_API_KEY", "")

def ok(): return jsonify({"ok": True})

@app.get("/health")
def health():
    return ok(), 200

def authed():
    return request.headers.get("X-API-Key", "") == API_KEY

def do_think(payload):
    text = (payload or {}).get("text", "")
    # 這裡放真正的思考/規劃邏輯；先回 echo
    return {"result": f"brain got: {text}"}

@app.post("/think")
def think():
    if not authed():
        return jsonify({"error":"unauthorized"}), 401
    return jsonify(do_think(request.get_json(silent=True))), 200

# 相容機器人目前可能呼叫的 /run
@app.post("/run")
def run_compat():
    if not authed():
        return jsonify({"error":"unauthorized"}), 401
    return jsonify(do_think(request.get_json(silent=True))), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
