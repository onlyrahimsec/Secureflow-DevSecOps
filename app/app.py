from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database import init_db, get_db_connection

app = Flask(__name__)

# Initialize database
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

        # Basic input validation
        if not username or not email or not password:
            return "All fields are required.", 400

        # Hash password before storing it
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

        return redirect(url_for("home"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
