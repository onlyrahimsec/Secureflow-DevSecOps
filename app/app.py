from flask import Flask, render_template
from database import init_db

app = Flask(__name__)

# Initialize database
init_db()


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
