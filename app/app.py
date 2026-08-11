from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import init_db, get_db_connection


app = Flask(__name__)

# Development-only secret.
# Production implementation will use environment-based secrets.
app.secret_key = "secureflow-development-key"

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return "All fields are required.", 400

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (username, email, password_hash)
            )

            connection.commit()

        except Exception:
            connection.close()
            return "Unable to create account.", 400

        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return "Username and password are required.", 400

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT id, username, password_hash, role
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(
            user["password_hash"],
            password
        ):
            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        return "Invalid username or password.", 401

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Access denied.", 403

    return render_template(
        "admin.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
