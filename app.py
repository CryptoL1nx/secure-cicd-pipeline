import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

# VULN-01 : secret en dur dans le code source
API_TOKEN = "a8f5f167f44f4964e6c998dee827110c3b9d8e1f"
DB_PATH = "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)"
    )
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users VALUES (1, 'alice', 'alice@example.com', 'alicepw')")
    conn.execute("INSERT INTO users VALUES (2, 'bob', 'bob@example.com', 'bobpw')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return jsonify({"status": "ok", "app": "vulnerable-demo"})


@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    # VULN-02 : injection SQL (requête construite par concaténation)
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify(rows)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # VULN-03 : injection de commande (shell=True avec entrée utilisateur)
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, text=True
    )
    return jsonify({"output": result.stdout})


if __name__ == "__main__":
    init_db()
    # VULN-04 : mode debug actif et écoute sur toutes les interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
