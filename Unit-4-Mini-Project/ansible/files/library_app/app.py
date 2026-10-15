from flask import Flask, jsonify, request
import os
import sqlite3

app = Flask(__name__)
DB_PATH = "/data/library.db"

os.makedirs("/data", exist_ok=True)

def get_db():
    return sqlite3.connect(DB_PATH)

with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

@app.route("/")
def home():
    return jsonify({
        "application": "Smart Library Management Platform",
        "status": "running"
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/books", methods=["GET"])
def list_books():
    with get_db() as db:
        rows = db.execute(
            "SELECT id, title, author FROM books"
        ).fetchall()
    return jsonify([
        {"id": row[0], "title": row[1], "author": row[2]}
        for row in rows
    ])

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({
            "error": "Both title and author are required"
        }), 400

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author)
        )
        book_id = cursor.lastrowid

    return jsonify({
        "id": book_id,
        "title": title,
        "author": author
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
