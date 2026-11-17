from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "skills.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'To Learn'
        )
        """)

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status FROM skills")
        skills = cursor.fetchall()
    return render_template("index.html", skills=skills)

@app.route("/add", methods=["POST"])
def add_skill():
    title = request.form.get("title")
    if title:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO skills (title, status) VALUES (?, 'To Learn')", (title,))
    return redirect(url_for("index"))

@app.route("/toggle/<int:skill_id>")
def toggle_status(skill_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM skills WHERE id = ?", (skill_id,))
        row = cursor.fetchone()
        if row:
            new_status = "Completed" if row[0] == "To Learn" else "To Learn"
            conn.execute("UPDATE skills SET status = ? WHERE id = ?", (new_status, skill_id))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)