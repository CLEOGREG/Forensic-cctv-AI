from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import psutil
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Secret key for local session management
app.secret_key = "cctv-ai-surveillance-local-secret-key"

DATABASE = "database/forensiciq.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():

    # If already logged in, go directly to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    connection = get_db_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    # Check username and password
    if user and check_password_hash(
        user["password_hash"],
        password
    ):

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        return redirect(url_for("dashboard"))

    # Invalid login
    return render_template(
        "login.html",
        error="Invalid username or password."
    )


@app.route("/dashboard")
def dashboard():

    # Prevent unauthorized access
    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"]
    )

@app.route("/face-search")
def face_search():

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "face_search.html",
        username=session.get("username"),
        role=session.get("role")
    )

@app.route("/logout")
def logout():

    # Clear login session
    session.clear()

    return redirect(url_for("home"))

@app.route("/api/storage")
def storage():

    # Require login
    if "user_id" not in session:
        return {
            "error": "Unauthorized"
        }, 401

    disk = psutil.disk_usage("/")

    total_gb = disk.total / (1024 ** 3)
    used_gb = disk.used / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)

    return {
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "percent": disk.percent,
        "status": "HEALTHY" if disk.percent < 85 else "WARNING"
    }

@app.route("/recordings")
def recordings():

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "recordings.html",
        username=session.get("username"),
        role=session.get("role")
    )

@app.route("/camera-management")
def camera_management():

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "camera_management.html",
        username=session.get("username"),
        role=session.get("role")
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )