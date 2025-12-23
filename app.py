from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

def get_db():
    return sqlite3.connect("urls.db")

# Create table
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT
        )
    """)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_code = generate_code()

        db = get_db()
        db.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
            (short_code, long_url)
        )
        db.commit()

        short_url = request.host_url + short_code

    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_url(short_code):
    db = get_db()
    result = db.execute(
        "SELECT long_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    if result:
        return redirect(result[0])
    return "URL not found", 404

if __name__ == "__main__":
    app.run()
