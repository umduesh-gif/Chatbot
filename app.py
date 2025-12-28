from flask import Flask, request, jsonify, send_from_directory
import sqlite3, json, os
from datetime import datetime

app = Flask(__name__, static_folder="static")
DB = "memory.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            ts TEXT
        )
    """)
    conn.commit()
    conn.close()

def save(role, content):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (role, content, ts) VALUES (?, ?, ?)",
        (role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    persona = data.get("persona", "default")
    nsfw = data.get("nsfw", False)

    save("user", msg)

    angel = f"😇 Angel ({persona}): I understand you. {msg}"
    demon = f"😈 Demon ({persona}): Interesting thought… {msg.upper()}"

    reply = {"angel": angel, "demon": demon}

    save("assistant", json.dumps(reply))

    return jsonify(reply)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
